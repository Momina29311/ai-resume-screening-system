from pathlib import Path
import json

import pandas as pd


SKILLS_FILE = Path("data/skills/skills.csv")
OUTPUT_DIR = Path("data/extracted_skills")


def load_skills(skills_file: Path = SKILLS_FILE) -> list[str]:
    df = pd.read_csv(skills_file)
    skills = df["Skill"].dropna().astype(str).tolist()
    return sorted(set(skill.strip() for skill in skills if skill.strip()))


def normalize_text(text: str) -> str:
    return text.lower()


def extract_skills(resume_text: str, skills: list[str] | None = None) -> list[str]:
    if skills is None:
        skills = load_skills()

    text = normalize_text(resume_text)
    found = []

    for skill in skills:
        if skill.lower() in text:
            found.append(skill)

    return remove_duplicates(found)


def remove_duplicates(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def sort_skills(skills: list[str]) -> list[str]:
    return sorted(skills, key=lambda x: x.lower())


def save_skills(resume_name: str, skills: list[str]) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{Path(resume_name).stem}_skills.json"

    payload = {
        "resume_name": resume_name,
        "skills": skills,
        "total_skills": len(skills),
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return str(output_path)