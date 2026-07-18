from pathlib import Path
import json


def normalize_skills(skills):
    return sorted({skill.strip().lower() for skill in skills if skill and skill.strip()})


def match_resume_to_job(resume_skills, job_skills):
    resume_set = set(normalize_skills(resume_skills))
    job_set = set(normalize_skills(job_skills))

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    match_score = round((len(matched) / len(job_set)) * 100, 1) if job_set else 0.0

    recommendations = [f"Learn {skill}." for skill in missing]

    return {
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
    }


def save_match_result(resume_name, result):
    output_dir = Path("data/matches")
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(resume_name).stem.replace(" ", "_")
    output_path = output_dir / f"{safe_name}_match.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return str(output_path)