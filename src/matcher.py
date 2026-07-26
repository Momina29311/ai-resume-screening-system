from pathlib import Path
import json
from typing import Any, Dict, List

from src.semantic_matcher import semantic_match_result


def normalize_skills(skills):
    return sorted({skill.strip().lower() for skill in skills if skill and skill.strip()})


def match_resume_to_job(
    resume_skills: List[str],
    job_skills: List[str],
    resume_text: str = "",
    job_description_text: str = "",
) -> Dict[str, Any]:
    """
    Match resume to job using:
      - keyword-based skill matching (existing logic)
      - semantic similarity between full resume and JD (new)
    """

    resume_set = set(normalize_skills(resume_skills))
    job_set = set(normalize_skills(job_skills))

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    keyword_match_score = round((len(matched) / len(job_set)) * 100, 1) if job_set else 0.0

    recommendations = [f"Learn {skill}." for skill in missing]

    # Semantic matching (only if texts are provided)
    semantic = semantic_match_result(resume_text, job_description_text) if (resume_text and job_description_text) else {"semantic_score": 0.0, "semantic_label": "Not computed"}

    return {
        "match_score": keyword_match_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
        "semantic_match_percent": semantic["semantic_score"],
        "semantic_match_label": semantic["semantic_label"],
    }


def save_match_result(resume_name, result):
    output_dir = Path("data/matches")
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(resume_name).stem.replace(" ", "_")
    output_path = output_dir / f"{safe_name}_match.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return str(output_path)