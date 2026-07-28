"""
Candidate ranking engine for ResumeIQ.

Day 85 upgrade — Explainable AI (XAI):
- generate_score_breakdown() shows exactly how the final score was built
  from its three weighted components (ATS / semantic / experience).
- generate_strengths_weaknesses() produces a clean strengths vs. weaknesses
  split per candidate, separate from the free-text feedback/suggestions.
- generate_recommendation_reason() gives a structured {label, reasons} pair
  driving the recommendation callout in the UI.
- compare_candidates_explanation() replaces raw side-by-side numbers with
  "X ranks higher because ..." reasoning for both candidates.
- compute_recruiter_top_strengths() rolls strengths up across the whole
  pool for the recruiter insights dashboard.
- export_explainability_report_json()/_csv() produce a downloadable,
  fully-explained report (per-candidate strengths/weaknesses/reason),
  separate from the raw ranking_results export.
- Every candidate dict returned by rank_candidates() now also carries
  score_breakdown, strengths, weaknesses, and recommendation_reason.

Day 84 upgrade — Hybrid AI Candidate Ranking:
- final_score now blends ATS score, semantic similarity, AND experience
  (60% / 30% / 10%) instead of just ATS + semantic.
- experience_score (0-100, normalized from years_experience) is now a
  first-class field on every candidate.
- explain_ranking() gives human-readable reasons for why a candidate
  ranked where they did (explainability for Day 85 lead-in).
- Aggregate insights now include final_score stats (highest/average),
  alongside the existing ats/match/semantic stats.
- CSV/JSON export include experience_score and final_score.

Day 84.1 patch — Experience extraction fix:
- extract_years_experience() now ALSO parses job-history date ranges
  (e.g. "Mar 2022 – Present", "Jul 2019 – Feb 2022") and computes career
  span from the earliest start date to the latest end date. Previously
  only explicit phrasing like "5 years of experience" was detected, which
  meant resumes using a standard work-history format (dates per role, no
  explicit year count) scored 0 experience even for senior candidates.
  The function now takes the max of both detection methods.

Carried over from the previous version:
- Skill alias normalization (e.g. "js" -> "javascript").
- Required vs. preferred skill parsing from the job description.
- Aggregate insight helpers (average score, most commonly missing skills).
"""
from src.matcher import match_resume_to_job
from pathlib import Path
from datetime import date
import csv
import json
import re

# Common shorthand -> canonical skill name. Extend as needed.
SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node",
    "node.js": "node",
    "postgres": "postgresql",
    "k8s": "kubernetes",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "amazon web services": "aws",
    "gcp": "google cloud",
    "nlp": "natural language processing",
}

PREFERRED_MARKERS = ["preferred", "nice to have", "nice-to-have", "bonus", "a plus", "good to have"]

# Method 1: explicit phrasing, e.g. "5 years of experience"
YEARS_PATTERNS = [
    re.compile(r"(\d{1,2})\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience", re.IGNORECASE),
    re.compile(r"experience\s*[:\-]?\s*(\d{1,2})\+?\s*(?:years?|yrs?)", re.IGNORECASE),
]

# Method 2: job-history date ranges, e.g. "Mar 2022 – Present", "Jul 2019 - Feb 2022"
MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12,
}

DATE_RANGE_PATTERN = re.compile(
    r"(?P<start_month>[A-Za-z]{3,9})\.?\s+(?P<start_year>\d{4})\s*[-–—]+\s*"
    r"(?P<end_month>[A-Za-z]{3,9}|Present|Current)\.?\s*(?P<end_year>\d{4})?",
    re.IGNORECASE,
)

DEGREE_WORDS = ["bachelor", "master", "bsc", "msc", "bs", "ms", "phd", "degree", "b.tech", "m.tech"]
PROJECT_WORDS = ["project", "built", "developed", "implemented", "dashboard", "api", "shipped", "launched"]
CERT_WORDS = ["certification", "certificate", "certified", "coursera", "udemy", "aws certified", "pmp"]

# Hybrid final-score weights: ATS, Semantic, Experience (must sum to 1.0)
FINAL_SCORE_WEIGHTS = (0.60, 0.30, 0.10)

# Years of experience treated as "fully maxed" for normalization purposes
MAX_YEARS_FOR_SCORING = 10


def normalize_skill(skill):
    s = skill.strip().lower()
    return SKILL_ALIASES.get(s, s)


def _extract_explicit_years(resume_text):
    """Method 1: largest 'X years experience' figure explicitly stated."""
    years_found = []
    for pattern in YEARS_PATTERNS:
        for match in pattern.finditer(resume_text):
            try:
                years_found.append(int(match.group(1)))
            except (ValueError, IndexError):
                continue
    return max(years_found) if years_found else 0


def _extract_date_range_years(resume_text):
    """
    Method 2: parses "Month YYYY – Month YYYY" / "Month YYYY – Present" style
    ranges commonly used in work-history sections, and returns the total span
    from the earliest start date to the latest end date (in years).
    """
    earliest_start = None
    latest_end = None
    today = date.today()

    for match in DATE_RANGE_PATTERN.finditer(resume_text):
        start_month_str = match.group("start_month").lower()[:3]
        start_year = match.group("start_year")
        end_month_raw = match.group("end_month")
        end_month_str = end_month_raw.lower()[:3] if end_month_raw else None
        end_year = match.group("end_year")

        if start_month_str not in MONTH_MAP or not start_year:
            continue

        try:
            start_dt = date(int(start_year), MONTH_MAP[start_month_str], 1)
        except ValueError:
            continue

        if end_month_str in ("pre", "cur"):  # "Present" / "Current"
            end_dt = today
        elif end_month_str in MONTH_MAP and end_year:
            try:
                end_dt = date(int(end_year), MONTH_MAP[end_month_str], 1)
            except ValueError:
                end_dt = start_dt
        else:
            end_dt = start_dt  # fallback: single date mention, no real range

        if earliest_start is None or start_dt < earliest_start:
            earliest_start = start_dt
        if latest_end is None or end_dt > latest_end:
            latest_end = end_dt

    if earliest_start and latest_end and latest_end > earliest_start:
        return round((latest_end - earliest_start).days / 365.25)
    return 0


def extract_years_experience(resume_text):
    """
    Best-effort extraction of total years of experience. Combines two
    detection methods and returns the larger of the two:
      1. Explicit phrasing ("5 years of experience").
      2. Career span computed from job-history date ranges
         ("Mar 2022 – Present", "Jul 2019 – Feb 2022", ...).
    This ensures resumes that only list role dates (no explicit year count)
    still get accurate experience credit.
    """
    explicit_years = _extract_explicit_years(resume_text)
    date_range_years = _extract_date_range_years(resume_text)
    return max(explicit_years, date_range_years)


def normalize_experience_score(years_experience, max_years=MAX_YEARS_FOR_SCORING):
    """Scale years of experience to a 0-100 score for use in the hybrid formula."""
    if not years_experience:
        return 0.0
    return round(min(years_experience / max_years, 1.0) * 100, 1)


def parse_job_requirements(job_description, skills_db):
    """
    Splits job-description skills into required vs. preferred sets based on
    common section markers ("preferred", "nice to have", ...). If no marker
    is found, every mentioned skill is treated as required.
    Returns (required_skills, preferred_skills) as lists (order preserved).
    """
    lower_full = job_description.lower()
    split_idx = len(job_description)
    for marker in PREFERRED_MARKERS:
        idx = lower_full.find(marker)
        if idx != -1:
            split_idx = min(split_idx, idx)

    required_text = job_description[:split_idx].lower()
    preferred_text = job_description[split_idx:].lower()

    required_skills, preferred_skills = [], []
    for skill in skills_db:
        skill_l = skill.lower()
        if skill_l in required_text:
            required_skills.append(skill)
        elif skill_l in preferred_text:
            preferred_skills.append(skill)

    return required_skills, preferred_skills


def calculate_match_percent(resume_skills, required_skills, preferred_skills):
    """
    Weighted match: required skills count double toward the score, preferred
    skills count once. Falls back gracefully if the job has no detected skills.
    """
    resume_set = {normalize_skill(s) for s in resume_skills}
    required_set = {normalize_skill(s) for s in required_skills}
    preferred_set = {normalize_skill(s) for s in preferred_skills} - required_set

    total_weight = len(required_set) * 2 + len(preferred_set)
    if total_weight == 0:
        return 0

    matched_weight = sum(2 for s in required_set if s in resume_set)
    matched_weight += sum(1 for s in preferred_set if s in resume_set)

    return min(int((matched_weight / total_weight) * 100), 100)


def calculate_ats_breakdown(match_percent, resume_text, years_experience):
    text_len = len(resume_text.split())
    lower = resume_text.lower()

    # Skills: up to 40 points, scaled from weighted match percent.
    skills_score = min(int(match_percent * 0.40), 40)

    # Experience: blend years-mentioned with resume length/detail, up to 20 points.
    years_score = min(years_experience * 3, 20)
    length_score = 0
    if text_len > 150:
        length_score = 8
    if text_len > 300:
        length_score = 14
    if text_len > 600:
        length_score = 18
    experience_score = min(max(years_score, length_score), 20)

    education_score = 15 if any(w in lower for w in DEGREE_WORDS) else 8
    projects_score = 10 if any(w in lower for w in PROJECT_WORDS) else 4
    certifications_score = 8 if any(w in lower for w in CERT_WORDS) else 2
    completeness_score = 7 if text_len > 150 else (4 if text_len > 50 else 1)

    total = (
        skills_score
        + experience_score
        + education_score
        + projects_score
        + certifications_score
        + completeness_score
    )
    total = min(total, 100)

    return {
        "skills": skills_score,
        "experience": experience_score,
        "education": education_score,
        "projects": projects_score,
        "certifications": certifications_score,
        "completeness": completeness_score,
        "total": total,
    }


def calculate_ats_score(match_percent, resume_text, years_experience=0):
    breakdown = calculate_ats_breakdown(match_percent, resume_text, years_experience)
    return breakdown["total"], breakdown


def calculate_final_score(ats_score, semantic_match_percent, experience_score,
                           weights=FINAL_SCORE_WEIGHTS):
    """
    Hybrid AI ranking score combining ATS, semantic similarity, and experience.
    weights = (ats_weight, semantic_weight, experience_weight), sums to 1.0.
    """
    w_ats, w_sem, w_exp = weights
    final = (ats_score * w_ats) + (semantic_match_percent * w_sem) + (experience_score * w_exp)
    return round(final, 1)


def generate_score_breakdown(ats_score, semantic_match_percent, experience_score,
                              weights=FINAL_SCORE_WEIGHTS):
    """
    Day 85 — Explainable AI: shows exactly how the final score was built,
    e.g.

        ATS Score Contribution   : 70 x 0.60 = 42.0
        Semantic Similarity      : 92 x 0.30 = 27.6
        Experience Bonus         : 100 x 0.10 = 10.0
        Final Score              : 79.6

    Returns a dict with each weighted contribution plus the recombined
    final score, so the UI can render it as a transparent line-by-line
    calculation instead of a single opaque number.
    """
    w_ats, w_sem, w_exp = weights

    ats_contribution = round(ats_score * w_ats, 1)
    semantic_contribution = round(semantic_match_percent * w_sem, 1)
    experience_contribution = round(experience_score * w_exp, 1)
    final = round(ats_contribution + semantic_contribution + experience_contribution, 1)

    return {
        "ats_score": ats_score,
        "ats_weight": w_ats,
        "ats_contribution": ats_contribution,
        "semantic_score": semantic_match_percent,
        "semantic_weight": w_sem,
        "semantic_contribution": semantic_contribution,
        "experience_score": experience_score,
        "experience_weight": w_exp,
        "experience_contribution": experience_contribution,
        "final_score": final,
    }


def get_recommendation_level(ats_score, match_percent):
    if ats_score >= 85 and match_percent >= 75:
        return "Highly Recommended"
    if ats_score >= 70 and match_percent >= 55:
        return "Consider"
    return "Not Recommended"


def build_feedback(ats_score, match_percent, matched_skills, missing_required, years_experience):
    feedback = []

    if ats_score >= 85:
        feedback.append("Strong overall profile with excellent alignment to the job description.")
    elif ats_score >= 70:
        feedback.append("Solid candidate with good alignment, but a few gaps remain.")
    else:
        feedback.append("Candidate needs stronger alignment with the target role.")

    if years_experience:
        feedback.append(f"Resume indicates approximately {years_experience} year(s) of relevant experience.")

    if matched_skills:
        feedback.append(f"Matched strengths include: {', '.join(matched_skills[:5])}.")

    if missing_required:
        feedback.append(f"Missing required skills: {', '.join(missing_required[:5])}.")

    if match_percent >= 70:
        feedback.append("Suitable for interview after technical review.")
    else:
        feedback.append("Needs improvement before recruiter shortlist.")

    return feedback


def build_suggestions(missing_required, missing_preferred, resume_text):
    suggestions = []

    for skill in missing_required[:4]:
        suggestions.append(f"Add {skill} experience to the resume — this is a required skill.")
    for skill in missing_preferred[:2]:
        suggestions.append(f"Consider highlighting {skill}, listed as a preferred skill.")

    lower = resume_text.lower()
    if "project" not in lower:
        suggestions.append("Include measurable project outcomes.")
    if "certif" not in lower:
        suggestions.append("Highlight certifications.")
    if not suggestions:
        suggestions.append("Strengthen quantified impact and role-specific details.")

    return suggestions


def generate_strengths_weaknesses(ats_score, semantic_match_percent, years_experience,
                                   matched_skills, missing_required_skills, missing_preferred_skills):
    """
    Day 85 — Explainable AI: a clean, structured strengths vs. weaknesses
    split, separate from the free-text feedback. Used to power the
    "Strengths" / "Weaknesses" sections of each candidate card.
    """
    strengths = []
    weaknesses = []

    if ats_score >= 85:
        strengths.append(f"Excellent ATS score ({ats_score})")
    elif ats_score >= 70:
        strengths.append(f"Solid ATS score ({ats_score})")
    else:
        weaknesses.append(f"Below-target ATS score ({ats_score})")

    if semantic_match_percent >= 80:
        strengths.append(f"High semantic relevance ({semantic_match_percent}%)")
    elif semantic_match_percent < 50:
        weaknesses.append(f"Low semantic similarity to job description ({semantic_match_percent}%)")

    if years_experience >= 5:
        strengths.append(f"Strong experience depth ({years_experience} years)")
    elif years_experience >= 2:
        strengths.append(f"Relevant work experience ({years_experience} years)")
    else:
        weaknesses.append("Limited or undetected work experience")

    if matched_skills:
        strengths.append(f"{len(matched_skills)} matched skill(s), including {', '.join(matched_skills[:3])}")

    if not missing_required_skills:
        strengths.append("All required skills matched")
    else:
        for skill in missing_required_skills[:5]:
            weaknesses.append(f"Missing {skill}")

    for skill in missing_preferred_skills[:3]:
        weaknesses.append(f"Missing preferred skill: {skill}")

    if not strengths:
        strengths.append("No standout strengths identified yet")
    if not weaknesses:
        weaknesses.append("No significant gaps detected")

    return strengths, weaknesses


def generate_recommendation_reason(recommendation_level, strengths, weaknesses):
    """
    Day 85 — Explainable AI: turns a bare recommendation label
    ("Highly Recommended") into a structured {label, reasons} pair the UI
    can render as a bulleted justification instead of just a badge.
    """
    if recommendation_level == "Highly Recommended":
        reasons = strengths[:4] if strengths else ["Consistently strong scores across the board"]
    elif recommendation_level == "Consider":
        reasons = (strengths[:2] + [f"Gap to close: {w}" for w in weaknesses[:2]]) or \
                   ["Reasonable overall fit, worth a closer look"]
    else:
        reasons = weaknesses[:4] if weaknesses else ["Overall alignment falls short of the role requirements"]

    return {"label": recommendation_level, "reasons": reasons}


def explain_ranking(candidate, all_candidates):
    """
    Generate human-readable, explainable bullet points for why a candidate
    ranked where they did relative to the rest of the pool.
    """
    if not all_candidates:
        return ["✔ Balanced overall profile"]

    reasons = []
    avg_ats = sum(c["ats_score"] for c in all_candidates) / len(all_candidates)
    avg_sem = sum(c["semantic_match_percent"] for c in all_candidates) / len(all_candidates)
    avg_exp = sum(c.get("experience_score", 0) for c in all_candidates) / len(all_candidates)

    if candidate["ats_score"] >= avg_ats:
        reasons.append("✔ High ATS score")
    if candidate["semantic_match_percent"] >= avg_sem:
        reasons.append("✔ Strong semantic similarity")
    if candidate.get("experience_score", 0) >= avg_exp:
        reasons.append("✔ Relevant experience")

    missing_required = candidate.get("missing_required_skills", candidate.get("missing_skills", []))
    if len(missing_required) <= 2:
        reasons.append("✔ Few missing skills")

    if not reasons:
        reasons.append("✔ Balanced overall profile")

    return reasons


def compare_candidates_explanation(candidate_a, candidate_b):
    """
    Day 85 — Explainable AI: structured head-to-head comparison.
    Instead of a bare numbers table, returns "+ reasons" for each
    candidate plus an overall winner, e.g.

        Ali ranks higher because:
          + Better semantic similarity
          + More experience
          + More required skills matched

        Sara:
          + Higher ATS score
    """
    reasons_a, reasons_b = [], []

    def _compare(label, val_a, val_b, higher_is_better=True):
        if val_a == val_b:
            return
        a_wins = (val_a > val_b) if higher_is_better else (val_a < val_b)
        if a_wins:
            reasons_a.append(label)
        else:
            reasons_b.append(label)

    _compare("Higher ATS score", candidate_a.get("ats_score", 0), candidate_b.get("ats_score", 0))
    _compare("Better semantic similarity", candidate_a.get("semantic_match_percent", 0), candidate_b.get("semantic_match_percent", 0))
    _compare("More experience", candidate_a.get("years_experience", 0), candidate_b.get("years_experience", 0))
    _compare(
        "More required skills matched",
        len(candidate_a.get("matched_skills", [])),
        len(candidate_b.get("matched_skills", [])),
    )
    _compare(
        "Fewer missing required skills",
        len(candidate_a.get("missing_required_skills", [])),
        len(candidate_b.get("missing_required_skills", [])),
        higher_is_better=False,
    )

    score_a = candidate_a.get("final_score", candidate_a.get("ats_score", 0))
    score_b = candidate_b.get("final_score", candidate_b.get("ats_score", 0))

    if score_a == score_b:
        winner = "Tie"
    else:
        winner = candidate_a["name"] if score_a > score_b else candidate_b["name"]

    return {
        "winner": winner,
        candidate_a["name"]: reasons_a or ["No standout advantages"],
        candidate_b["name"]: reasons_b or ["No standout advantages"],
    }


def rank_candidates(parsed_resumes, job_description, skills_db):
    required_skills, preferred_skills = parse_job_requirements(job_description, skills_db)
    job_skills = required_skills + preferred_skills

    required_norm = {normalize_skill(s) for s in required_skills}
    preferred_norm = {normalize_skill(s) for s in preferred_skills} - required_norm

    ranked = []

    for resume in parsed_resumes:
        resume_skills = resume.get("skills", [])
        resume_text = resume.get("text", "")
        resume_name = resume.get("name", "Unknown Candidate")

        resume_set = {normalize_skill(s) for s in resume_skills}
        # Semantic + keyword matching
        match_result = match_resume_to_job(
            resume_skills=resume_skills,
            job_skills=job_skills,
            resume_text=resume_text,
            job_description_text=job_description,
        )

        semantic_score = match_result["semantic_match_percent"]
        semantic_label = match_result["semantic_match_label"]

        matched_skills = sorted(s for s in (required_norm | preferred_norm) if s in resume_set)
        missing_required = sorted(s for s in required_norm if s not in resume_set)
        missing_preferred = sorted(s for s in preferred_norm if s not in resume_set)
        missing_skills = missing_required + missing_preferred

        keyword_score = calculate_match_percent(
            resume_skills,
            required_skills,
            preferred_skills,
        )

        # 70% keyword + 30% semantic, used to feed the ATS "skills" sub-score
        match_percent = round(
            keyword_score * 0.7 +
            semantic_score * 0.3
        )

        years_experience = extract_years_experience(resume_text)
        ats_score, breakdown = calculate_ats_score(match_percent, resume_text, years_experience)
        experience_score = normalize_experience_score(years_experience)

        # Final ranking score = Hybrid AI Score.
        # Blends ATS (rule-based), semantic similarity (conceptual fit),
        # and normalized years of experience, so a candidate who reads as
        # a strong conceptual fit for the role — even with different
        # wording/skills or more tenure — can outrank a keyword-only match.
        final_score = calculate_final_score(ats_score, semantic_score, experience_score)
        score_breakdown = generate_score_breakdown(ats_score, semantic_score, experience_score)

        recommendation_level = get_recommendation_level(ats_score, match_percent)
        feedback = build_feedback(ats_score, match_percent, matched_skills, missing_required, years_experience)
        suggestions = build_suggestions(missing_required, missing_preferred, resume_text)

        strengths, weaknesses = generate_strengths_weaknesses(
            ats_score, semantic_score, years_experience,
            matched_skills, missing_required, missing_preferred,
        )
        recommendation_reason = generate_recommendation_reason(recommendation_level, strengths, weaknesses)

        ranked.append(
            {
                "name": resume_name,
                "ats_score": ats_score,
                "match_percent": match_percent,
                "years_experience": years_experience,
                "experience_score": experience_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "missing_required_skills": missing_required,
                "missing_preferred_skills": missing_preferred,
                "ats_breakdown": breakdown,
                "recommendation_level": recommendation_level,
                "feedback": feedback,
                "recommendations": suggestions,
                "keyword_match_score": keyword_score,
                "semantic_match_score": semantic_score,
                "semantic_match_percent": semantic_score,
                "semantic_match_label": semantic_label,
                "final_score": final_score,
                "score_breakdown": score_breakdown,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "recommendation_reason": recommendation_reason,
            }
        )

    ranked = sorted(ranked, key=lambda x: x["final_score"], reverse=True)

    best_score = ranked[0]["final_score"] if ranked else 0
    for i, item in enumerate(ranked, start=1):
        item["rank"] = i
        item["score_gap_from_best"] = round(best_score - item["final_score"], 1)
        item["ranking_reasons"] = explain_ranking(item, ranked)

    return ranked


def compute_aggregate_insights(ranked_results):
    """Cross-candidate stats for a dashboard/insights view."""
    if not ranked_results:
        return {
            "avg_ats_score": 0,
            "avg_match_percent": 0,
            "avg_semantic_match_percent": 0,
            "highest_semantic_match_percent": 0,
            "avg_final_score": 0,
            "highest_final_score": 0,
            "top_missing_skills": [],
            "candidate_count": 0,
        }

    avg_ats = sum(r["ats_score"] for r in ranked_results) / len(ranked_results)
    avg_match = sum(r["match_percent"] for r in ranked_results) / len(ranked_results)
    avg_semantic = sum(r.get("semantic_match_percent", 0) for r in ranked_results) / len(ranked_results)
    highest_semantic = max((r.get("semantic_match_percent", 0) for r in ranked_results), default=0)

    avg_final = sum(r.get("final_score", 0) for r in ranked_results) / len(ranked_results)
    highest_final = max((r.get("final_score", 0) for r in ranked_results), default=0)

    missing_counter = {}
    for r in ranked_results:
        for skill in r.get("missing_required_skills", []) or r.get("missing_skills", []):
            missing_counter[skill] = missing_counter.get(skill, 0) + 1

    top_missing = sorted(missing_counter.items(), key=lambda kv: kv[1], reverse=True)[:8]

    return {
        "avg_ats_score": round(avg_ats, 1),
        "avg_match_percent": round(avg_match, 1),
        "avg_semantic_match_percent": round(avg_semantic, 1),
        "highest_semantic_match_percent": round(highest_semantic, 1),
        "avg_final_score": round(avg_final, 1),
        "highest_final_score": round(highest_final, 1),
        "top_missing_skills": top_missing,  # list of (skill, count)
        "candidate_count": len(ranked_results),
    }


def compute_recruiter_top_strengths(ranked_results, top_n=8):
    """
    Day 85 — Explainable AI: rolls up the most common strengths across the
    whole candidate pool, for the "Top strengths across candidates" panel
    on the Insights tab.
    """
    strength_counter = {}
    for r in ranked_results:
        for strength in r.get("strengths", []):
            strength_counter[strength] = strength_counter.get(strength, 0) + 1

    return sorted(strength_counter.items(), key=lambda kv: kv[1], reverse=True)[:top_n]


def save_ranking_results(ranked_results, output_path="outputs/ranking_results.json"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ranked_results, f, indent=2)
    return output_path


def export_ranking_csv(ranked_results, output_path="outputs/ranking_results.csv"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "name",
        "ats_score",
        "match_percent",
        "semantic_match_percent",
        "experience_score",
        "final_score",
        "years_experience",
        "recommendation_level",
        "matched_skills",
        "missing_required_skills",
        "missing_preferred_skills",
    ]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in ranked_results:
            writer.writerow(
                {
                    "rank": item.get("rank"),
                    "name": item.get("name"),
                    "ats_score": item.get("ats_score"),
                    "match_percent": item.get("match_percent"),
                    "semantic_match_percent": item.get("semantic_match_percent"),
                    "experience_score": item.get("experience_score"),
                    "final_score": item.get("final_score"),
                    "years_experience": item.get("years_experience"),
                    "recommendation_level": item.get("recommendation_level"),
                    "matched_skills": "; ".join(item.get("matched_skills", [])),
                    "missing_required_skills": "; ".join(item.get("missing_required_skills", [])),
                    "missing_preferred_skills": "; ".join(item.get("missing_preferred_skills", [])),
                }
            )
    return output_path


def export_explainability_report_json(ranked_results, output_path="outputs/explainability_report.json"):
    """
    Day 85 — full explainability report: for every candidate, the score
    breakdown, strengths, weaknesses, and recommendation reason — the
    "why", not just the "what".
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    report = [
        {
            "rank": item.get("rank"),
            "candidate": item.get("name"),
            "ats_score": item.get("ats_score"),
            "semantic_match_percent": item.get("semantic_match_percent"),
            "experience_score": item.get("experience_score"),
            "final_score": item.get("final_score"),
            "score_breakdown": item.get("score_breakdown"),
            "strengths": item.get("strengths"),
            "weaknesses": item.get("weaknesses"),
            "recommendation": item.get("recommendation_reason"),
        }
        for item in ranked_results
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return output_path


def export_explainability_report_csv(ranked_results, output_path="outputs/explainability_report.csv"):
    """
    Day 85 — CSV variant of the explainability report: one row per
    candidate with final score, top reason, and recommendation label.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["rank", "candidate", "final_score", "reason", "recommendation"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in ranked_results:
            rec = item.get("recommendation_reason", {})
            reasons = rec.get("reasons", [])
            writer.writerow(
                {
                    "rank": item.get("rank"),
                    "candidate": item.get("name"),
                    "final_score": item.get("final_score"),
                    "reason": reasons[0] if reasons else "",
                    "recommendation": rec.get("label", item.get("recommendation_level")),
                }
            )
    return output_path