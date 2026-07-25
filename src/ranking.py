from pathlib import Path
import json

from .ats_score import ATSScorer
from .matcher import match_resume_to_job
from .utils import extract_resume_features


def calculate_match_percent(resume_skills, job_skills):
    if not job_skills:
        return 0

    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])

    matched = resume_set.intersection(job_set)
    percent = int((len(matched) / len(job_set)) * 100)
    return min(percent, 100)


def get_recommendation(ats_score):
    """Map an overall ATS score to a recruiter-facing recommendation tier."""
    if ats_score >= 80:
        return {"label": "Highly Recommended", "emoji": "🟢"}
    if ats_score >= 60:
        return {"label": "Recommended", "emoji": "🟡"}
    if ats_score >= 40:
        return {"label": "Needs Improvement", "emoji": "🟠"}
    return {"label": "Not Recommended", "emoji": "🔴"}


def build_breakdown_display(breakdown):
    """Turn an ATSScoreBreakdown into a UI-friendly score/max mapping."""
    return {
        "skills": {"score": breakdown.skill_match, "max": 40},
        "experience": {"score": breakdown.experience, "max": 20},
        "education": {"score": breakdown.education, "max": 15},
        "projects": {"score": breakdown.projects, "max": 10},
        "certifications": {"score": breakdown.certifications, "max": 10},
        "completeness": {"score": breakdown.completeness, "max": 5},
    }


def rank_candidates(parsed_resumes, job_description, skills_db):
    job_lower = job_description.lower()
    job_skills = [skill for skill in skills_db if skill.lower() in job_lower]

    scorer = ATSScorer()
    ranked = []

    for resume in parsed_resumes:
        resume_skills = resume.get("skills", [])
        resume_text = resume.get("text", "")

        match_result = match_resume_to_job(resume_skills, job_skills)
        match_result["skills_found"] = len(match_result["matched_skills"])

        features = extract_resume_features(resume_text)
        result = scorer.score(features, match_result)

        recommendation = get_recommendation(result.ats_score)

        ranked.append(
            {
                "name": resume["name"],
                "ats_score": result.ats_score,
                "match_percent": int(round(match_result["match_score"])),
                "matched_skills": match_result["matched_skills"],
                "missing_skills": match_result["missing_skills"],
                "breakdown": build_breakdown_display(result.breakdown),
                "feedback": result.feedback,
                "suggestions": result.recommendations,
                "recommendation": recommendation,
            }
        )

    ranked = sorted(ranked, key=lambda x: x["ats_score"], reverse=True)

    for i, item in enumerate(ranked, start=1):
        item["rank"] = i

    return ranked


def save_ranking_results(ranked_results, output_path="outputs/ranking_results.json"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ranked_results, f, indent=2)
    return output_path
