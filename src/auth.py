"""
Recruiter authentication for ResumeIQ (Day 86).

Design choices:
- Password hashing uses hashlib.pbkdf2_hmac (stdlib) with a per-user random
  salt and 260,000 iterations — no bcrypt/passlib dependency required, per
  the "hashlib if you want to avoid extra dependencies" option.
- Session state lives in Streamlit's st.session_state for the current
  browser session, with an optional "Remember Me" token (stored in
  src/database.py's sessions table and mirrored into the URL query param)
  so a page refresh or revisit doesn't force a re-login.
- A default admin account is auto-seeded on first run if the users table
  is empty, so the app isn't locked out of itself on a fresh clone.
- Failed login attempts are tracked per-account; after MAX_FAILED_ATTEMPTS
  the account is locked for LOCKOUT_MINUTES.
"""
import hashlib
import hmac
import secrets
from datetime import datetime

import streamlit as st

from src.database import (
    init_db,
    create_user,
    get_user,
    update_last_login,
    record_failed_attempt,
    reset_failed_attempts,
    is_user_locked,
    create_session_token,
    validate_session_token,
    delete_session_token,
    user_count,
)

PBKDF2_ITERATIONS = 260_000
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15
MIN_PASSWORD_LENGTH = 6
MIN_USERNAME_LENGTH = 3

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "ChangeMe123!"

SESSION_KEYS = [
    "authenticated",
    "username",
    "full_name",
    "last_login",
    "login_time",
    "remember_token",
]


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(password, salt=None):
    """Returns (hash_hex, salt_hex). Generates a new random salt if none is given."""
    if salt is None:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ITERATIONS
    ).hex()
    return pwd_hash, salt


def verify_password(password, stored_hash, salt):
    candidate_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(candidate_hash, stored_hash)


# ---------------------------------------------------------------------------
# Account creation / seeding
# ---------------------------------------------------------------------------

def register_recruiter(username, password, full_name):
    """Creates a new recruiter account. Returns True on success, False if the username is taken."""
    init_db()
    pwd_hash, salt = hash_password(password)
    return create_user(username, pwd_hash, salt, full_name)


def attempt_registration(username, password, confirm_password, full_name):
    """
    Validates and creates a self-service recruiter account.
    Returns (success: bool, message: str).
    """
    username = (username or "").strip()
    full_name = (full_name or "").strip()

    if not username or not password or not full_name:
        return False, "Please fill in your name, username, and password."
    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Username must be at least {MIN_USERNAME_LENGTH} characters."
    if " " in username:
        return False, "Username can't contain spaces."
    if password != confirm_password:
        return False, "Passwords don't match."
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    if get_user(username) is not None:
        return False, f"Username '{username}' is already taken."

    created = register_recruiter(username, password, full_name)
    if not created:
        return False, "Could not create that account — the username may already be taken."
    return True, "Account created."


def seed_default_admin():
    """On a fresh database, creates a default admin account so the app isn't self-locked out."""
    init_db()
    if user_count() == 0:
        pwd_hash, salt = hash_password(DEFAULT_ADMIN_PASSWORD)
        create_user(DEFAULT_ADMIN_USERNAME, pwd_hash, salt, full_name="Admin")
        print(
            f"[ResumeIQ] No recruiter accounts found — created a default admin account.\n"
            f"           username: '{DEFAULT_ADMIN_USERNAME}'\n"
            f"           password: '{DEFAULT_ADMIN_PASSWORD}'\n"
            f"           Please log in and create a personal account via "
            f"scripts/manage_users.py, then retire this one."
        )


# ---------------------------------------------------------------------------
# Login logic (lockout-aware)
# ---------------------------------------------------------------------------

def attempt_login(username, password):
    """
    Validates credentials against the users table, tracking failed attempts
    and enforcing lockout. Returns (success, message, previous_last_login).
    """
    username = (username or "").strip()
    if not username or not password:
        return False, "Please enter both a username and password.", None

    user = get_user(username)
    if user is None:
        return False, "Invalid username or password.", None

    locked, unlock_time = is_user_locked(username)
    if locked:
        return False, f"Account locked from repeated failed attempts. Try again after {unlock_time}.", None

    if verify_password(password, user["password_hash"], user["salt"]):
        previous_last_login = user.get("last_login")
        reset_failed_attempts(username)
        update_last_login(username)
        return True, "Login successful.", previous_last_login

    attempts = record_failed_attempt(username, MAX_FAILED_ATTEMPTS, LOCKOUT_MINUTES)
    remaining = max(MAX_FAILED_ATTEMPTS - attempts, 0)
    if remaining == 0:
        return False, f"Account locked for {LOCKOUT_MINUTES} minutes due to repeated failed attempts.", None
    return False, f"Invalid username or password. {remaining} attempt(s) remaining before lockout.", None


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

def is_authenticated():
    return bool(st.session_state.get("authenticated", False))


def create_session(username, remember_me=False, last_login=None):
    user = get_user(username)
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.full_name = user["full_name"] if user else username
    st.session_state.last_login = last_login
    st.session_state.login_time = datetime.now().isoformat()

    if remember_me:
        token = create_session_token(username)
        st.session_state.remember_token = token
        st.query_params["token"] = token


def _restore_session_from_token(username, token):
    user = get_user(username)
    if user is None:
        return
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.full_name = user["full_name"]
    st.session_state.last_login = user.get("last_login")
    st.session_state.login_time = datetime.now().isoformat()
    st.session_state.remember_token = token


def logout():
    token = st.session_state.get("remember_token")
    if token:
        delete_session_token(token)
    for key in SESSION_KEYS:
        st.session_state.pop(key, None)
    st.query_params.clear()
    st.rerun()


# ---------------------------------------------------------------------------
# UI: login page + sidebar identity panel
# ---------------------------------------------------------------------------

def render_login_page():
    """
    Renders the ResumeIQ login screen and handles the full login flow,
    including restoring a "Remember Me" session from the URL token.

    Returns True once the user is authenticated (freshly logged in or
    restored via token), False while still on the login screen — callers
    should st.stop() when this returns False.
    """
    init_db()
    seed_default_admin()

    if not is_authenticated():
        token = st.query_params.get("token")
        if token:
            username = validate_session_token(token)
            if username:
                _restore_session_from_token(username, token)

    if is_authenticated():
        return True

    st.markdown('<div class="hero-badge fade-in-1">Case File • Restricted Access</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-title fade-in-2" style="font-size:2.2rem;">Sign in to <span class="hl">the desk</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("Authorized recruiters only. New here? Create your own account below.")

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    _, form_col, _ = st.columns([1, 1.4, 1])
    with form_col:
        toggle_col1, toggle_col2 = st.columns(2)
        if toggle_col1.button(
            "Log In",
            use_container_width=True,
            type="primary" if st.session_state.auth_mode == "login" else "secondary",
        ):
            st.session_state.auth_mode = "login"
            st.rerun()
        if toggle_col2.button(
            "Create Account",
            use_container_width=True,
            type="primary" if st.session_state.auth_mode == "signup" else "secondary",
        ):
            st.session_state.auth_mode = "signup"
            st.rerun()

        if st.session_state.auth_mode == "login":
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                remember_me = st.checkbox("Remember me on this device")
                submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)

            if submitted:
                success, message, previous_last_login = attempt_login(username, password)
                if success:
                    create_session(username, remember_me=remember_me, last_login=previous_last_login)
                    st.rerun()
                else:
                    st.error(message)

        else:
            with st.form("signup_form"):
                full_name = st.text_input("Full Name")
                new_username = st.text_input("Choose a Username")
                new_password = st.text_input("Choose a Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                signup_submitted = st.form_submit_button(
                    "Create Account", type="primary", use_container_width=True
                )

            if signup_submitted:
                success, message = attempt_registration(
                    new_username, new_password, confirm_password, full_name
                )
                if success:
                    create_session(new_username.strip(), remember_me=False, last_login=None)
                    st.success("Account created — welcome to ResumeIQ.")
                    st.rerun()
                else:
                    st.error(message)

    return False


def render_sidebar_user_info():
    """Shows the logged-in recruiter's name, last login time, and a Log Out button in the sidebar."""
    st.sidebar.markdown("---")
    display_name = st.session_state.get("full_name") or st.session_state.get("username", "")
    st.sidebar.markdown(f"**👤 {display_name}**")

    last_login = st.session_state.get("last_login")
    if last_login:
        try:
            dt = datetime.fromisoformat(last_login)
            st.sidebar.caption(f"Last login: {dt.strftime('%b %d, %Y · %H:%M')}")
        except ValueError:
            st.sidebar.caption(f"Last login: {last_login}")
    else:
        st.sidebar.caption("This is your first login.")

    if st.sidebar.button("Log Out", use_container_width=True):
        logout()