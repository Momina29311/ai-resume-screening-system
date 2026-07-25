"""
Candidate ranking engine for ResumeIQ.

Upgrades over the baseline version:
- Skill alias normalization (e.g. "js" -> "javascript") so near-identical
  skills aren't treated as mismatches.
- Required vs. preferred skill parsing from the job description, with
  required skills weighted higher in the match score.
- Years-of-experience extraction from resume text (regex based), blended
  into the "experience" ATS category instead of relying on word count alone.
- Aggregate insight helpers so the UI can show cross-candidate stats
  (average score, most commonly missing skills, etc.).
- CSV export alongside the existing JSON export.
"""

from pathlib import Path
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

YEARS_PATTERNS = [
    re.compile(r"(\d{1,2})\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience", re.IGNORECASE),
    re.compile(r"experience\s*[:\-]?\s*(\d{1,2})\+?\s*(?:years?|yrs?)", re.IGNORECASE),
]

DEGREE_WORDS = ["bachelor", "master", "bsc", "msc", "bs", "ms", "phd", "degree", "b.tech", "m.tech"]
PROJECT_WORDS = ["project", "built", "developed", "implemented", "dashboard", "api", "shipped", "launched"]
CERT_WORDS = ["certification", "certificate", "certified", "coursera", "udemy", "aws certified", "pmp"]


def normalize_skill(skill):
    s = skill.strip().lower()
    return SKILL_ALIASES.get(s, s)


def extract_years_experience(resume_text):
    """Best-effort extraction of the largest 'X years experience' figure mentioned."""
    years_found = []
    for pattern in YEARS_PATTERNS:
        for match in pattern.finditer(resume_text):
            try:
                years_found.append(int(match.group(1)))
            except (ValueError, IndexError):
                continue
    return max(years_found) if years_found else 0


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

        matched_skills = sorted(s for s in (required_norm | preferred_norm) if s in resume_set)
        missing_required = sorted(s for s in required_norm if s not in resume_set)
        missing_preferred = sorted(s for s in preferred_norm if s not in resume_set)
        missing_skills = missing_required + missing_preferred

        match_percent = calculate_match_percent(resume_skills, required_skills, preferred_skills)
        years_experience = extract_years_experience(resume_text)
        ats_score, breakdown = calculate_ats_score(match_percent, resume_text, years_experience)

        recommendation_level = get_recommendation_level(ats_score, match_percent)
        feedback = build_feedback(ats_score, match_percent, matched_skills, missing_required, years_experience)
        suggestions = build_suggestions(missing_required, missing_preferred, resume_text)

        ranked.append(
            {
                "name": resume_name,
                "ats_score": ats_score,
                "match_percent": match_percent,
                "years_experience": years_experience,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "missing_required_skills": missing_required,
                "missing_preferred_skills": missing_preferred,
                "ats_breakdown": breakdown,
                "recommendation_level": recommendation_level,
                "feedback": feedback,
                "recommendations": suggestions,
            }
        )

    ranked = sorted(ranked, key=lambda x: x["ats_score"], reverse=True)

    best_score = ranked[0]["ats_score"] if ranked else 0
    for i, item in enumerate(ranked, start=1):
        item["rank"] = i
        item["score_gap_from_best"] = best_score - item["ats_score"]

    return ranked


def compute_aggregate_insights(ranked_results):
    """Cross-candidate stats for a dashboard/insights view."""
    if not ranked_results:
        return {
            "avg_ats_score": 0,
            "avg_match_percent": 0,
            "top_missing_skills": [],
            "candidate_count": 0,
        }

    avg_ats = sum(r["ats_score"] for r in ranked_results) / len(ranked_results)
    avg_match = sum(r["match_percent"] for r in ranked_results) / len(ranked_results)

    missing_counter = {}
    for r in ranked_results:
        for skill in r.get("missing_required_skills", []) or r.get("missing_skills", []):
            missing_counter[skill] = missing_counter.get(skill, 0) + 1

    top_missing = sorted(missing_counter.items(), key=lambda kv: kv[1], reverse=True)[:8]

    return {
        "avg_ats_score": round(avg_ats, 1),
        "avg_match_percent": round(avg_match, 1),
        "top_missing_skills": top_missing,  # list of (skill, count)
        "candidate_count": len(ranked_results),
    }


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
                    "years_experience": item.get("years_experience"),
                    "recommendation_level": item.get("recommendation_level"),
                    "matched_skills": "; ".join(item.get("matched_skills", [])),
                    "missing_required_skills": "; ".join(item.get("missing_required_skills", [])),
                    "missing_preferred_skills": "; ".join(item.get("missing_preferred_skills", [])),
                }
            )
    return output_path