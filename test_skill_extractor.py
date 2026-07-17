from src.skill_extractor import load_skills, extract_skills, save_skills

sample_text = """
Experienced data analyst with Python, SQL, Pandas, NumPy, TensorFlow, Docker,
Git, and Machine Learning background.
"""

skills = load_skills()
found = extract_skills(sample_text, skills)

print("Detected skills:", found)
print("Saved file:", save_skills("sample_resume.pdf", found))