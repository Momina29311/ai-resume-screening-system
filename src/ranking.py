from pathlib import Path
import json

def calculate_match_percent(resume_skills, job_skills):
    if not job_skills:
        return 0

    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])

    matched = resume_set.intersection(job_set)
    percent = int((len(matched) / len(job_set)) * 100)
    return min(percent, 100)

def calculate_ats_score(match_percent, resume_text):
    text_len = len(resume_text.split())
    bonus = 0

    if text_len > 300:
        bonus += 5
    if text_len > 600:
        bonus += 5

    score = min(match_percent + bonus, 100)
    return score

def rank_candidates(parsed_resumes, job_description, skills_db):
    job_skills = []
    job_lower = job_description.lower()

    for skill in skills_db:
        if skill.lower() in job_lower:
            job_skills.append(skill)

    ranked = []

    for resume in parsed_resumes:
        resume_skills = resume.get("skills", [])
        resume_text = resume.get("text", "")

        match_percent = calculate_match_percent(resume_skills, job_skills)
        ats_score = calculate_ats_score(match_percent, resume_text)

        matched_skills = sorted(list(set([s.lower() for s in resume_skills]).intersection(set([s.lower() for s in job_skills]))))
        missing_skills = sorted(list(set([s.lower() for s in job_skills]).difference(set([s.lower() for s in resume_skills]))))

        ranked.append(
            {
                "name": resume["name"],
                "ats_score": ats_score,
                "match_percent": match_percent,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "feedback": [
                    "Good match with the job description." if match_percent >= 70 else "Improve skill alignment with the job description."
                ],
                "recommendations": [
                    "Highlight matched skills more clearly in your resume."
                    if match_percent < 85 else "Strong candidate for interview."
                ],
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