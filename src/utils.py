from pathlib import Path
from datetime import datetime
import re

def create_directory(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def write_text(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")

def log_message(message: str) -> None:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")


def extract_resume_features(resume_text: str) -> dict:
    """
    Lightweight heuristic extraction of resume structure from raw text.

    Produces the shape expected by ATSScorer.score(): sections_present,
    education, experience, projects, certifications. This lets the
    dashboard show a transparent, category-wise ATS breakdown without
    requiring a full resume-structure parser.
    """
    text = resume_text or ""
    text_lower = text.lower()

    sections_present = {
        "contact_info": bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)) or "phone" in text_lower,
        "summary": any(k in text_lower for k in ["summary", "objective", "profile"]),
        "skills": "skill" in text_lower,
        "education": any(
            k in text_lower
            for k in ["education", "bachelor", "master", "degree", "university", "college", "phd"]
        ),
        "experience": any(
            k in text_lower for k in ["experience", "worked", "internship", "employed"]
        ),
    }

    education = []
    if "phd" in text_lower or "doctor" in text_lower:
        education.append({"degree": "PhD"})
    elif any(k in text_lower for k in ["master", "m.sc", "m.tech", "msc"]):
        education.append({"degree": "Master"})
    elif any(k in text_lower for k in ["bachelor", "b.sc", "b.tech", "bsc"]) or re.search(r"\bbs\b", text_lower):
        education.append({"degree": "Bachelor"})
    elif any(k in text_lower for k in ["degree", "university", "college"]):
        education.append({"degree": "Unspecified"})

    experience = []
    years_matches = re.findall(r"(\d+)\+?\s*year", text_lower)
    if years_matches:
        max_years = max(int(y) for y in years_matches)
        experience.append({"title": "Experience", "duration_months": max_years * 12})
    elif "internship" in text_lower or "intern" in text_lower:
        experience.append({"title": "Internship", "duration_months": 4})
    elif any(k in text_lower for k in ["experience", "worked", "employed"]):
        experience.append({"title": "Experience", "duration_months": 6})

    project_mentions = len(re.findall(r"\bproject\b", text_lower))
    projects = [{"name": f"Project {i + 1}"} for i in range(min(project_mentions, 3))]

    cert_mentions = len(re.findall(r"certifi", text_lower))
    certifications = [{"name": f"Certification {i + 1}"} for i in range(min(cert_mentions, 2))]

    return {
        "sections_present": sections_present,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    }