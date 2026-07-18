from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from src.parser import extract_text_from_pdf, save_extracted_text
from src.skill_extractor import extract_skills, save_skills, load_skills
from src.matcher import match_resume_to_job, save_match_result


st.set_page_config(page_title="Resume Screening System", layout="wide")
st.title("Resume Screening System")
st.write("Upload a PDF resume to extract text, detect skills, and compare it with a job description.")


if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []
if "skills_db" not in st.session_state:
    st.session_state.skills_db = load_skills()
if "job_description" not in st.session_state:
    st.session_state.job_description = ""


uploaded_file = st.file_uploader("Upload a resume PDF", type=["pdf"])

col1, col2 = st.columns(2)
run_parse = col1.button("Parse Resume", type="primary")
compare_btn = col2.button("Compare Resume")
clear_btn = st.button("Clear")

if clear_btn:
    st.session_state.resume_text = ""
    st.session_state.resume_skills = []
    st.session_state.job_description = ""
    st.rerun()

if uploaded_file is None:
    st.info("Upload a PDF to begin.")
else:
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File type: {uploaded_file.type}")

    st.subheader("Job Description")
    st.session_state.job_description = st.text_area(
        "Paste the job description below",
        value=st.session_state.job_description,
        height=250,
        placeholder="Paste the job description here..."
    )

    if run_parse:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            text = extract_text_from_pdf(tmp_path)
            skills_db = st.session_state.skills_db
            skills = extract_skills(text, skills_db)

            st.session_state.resume_text = text
            st.session_state.resume_skills = skills

            save_path = save_extracted_text(tmp_path)
            skills_path = save_skills(uploaded_file.name, skills)

            st.success("Resume parsed successfully.")
            st.write(f"Characters extracted: {len(text)}")
            st.write(f"Words extracted: {len(text.split())}")

            stat1, stat2, stat3 = st.columns(3)
            stat1.metric("Skills Detected", len(skills))
            stat2.metric("Unique Skills", len(set(skills)))
            stat3.metric("Database Size", len(skills_db))

            st.subheader("Preview")
            st.text_area("Extracted text", text, height=400)

            st.subheader("Detected Skills")
            if skills:
                badge_cols = st.columns(3)
                for i, skill in enumerate(skills):
                    with badge_cols[i % 3]:
                        st.badge(skill, color="blue")
            else:
                st.warning("No skills detected.")

            st.subheader("Skill Comparison")
            comparison_data = []
            lower_text = text.lower()
            for skill in skills_db[:50]:
                comparison_data.append(
                    {
                        "Skill": skill,
                        "Found": "✅" if skill.lower() in lower_text else "❌",
                    }
                )
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

            st.info(f"Saved extracted text to: {save_path}")
            st.info(f"Saved skills to: {skills_path}")

            st.download_button(
                label="Download extracted text",
                data=text,
                file_name=Path(uploaded_file.name).stem + ".txt",
                mime="text/plain",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    if compare_btn:
        if not st.session_state.resume_text:
            st.warning("Please parse the resume first.")
        elif not st.session_state.job_description.strip():
            st.warning("Please paste a job description first.")
        else:
            resume_skills = st.session_state.resume_skills
            skills_db = st.session_state.skills_db
            job_skills = extract_skills(st.session_state.job_description, skills_db)

            result = match_resume_to_job(resume_skills, job_skills)
            result_path = save_match_result(uploaded_file.name, result)

            score = result["match_score"]
            score_int = max(0, min(100, int(round(score))))

            st.subheader("Resume Match")
            st.metric("Match Score", f"{score:.1f}%")
            st.progress(score_int)

            st.subheader("Matched Skills")
            if result["matched_skills"]:
                st.write(", ".join(result["matched_skills"]))
            else:
                st.write("None")

            st.subheader("Missing Skills")
            if result["missing_skills"]:
                st.write(", ".join(result["missing_skills"]))
            else:
                st.write("None")

            st.subheader("Recommendations")
            if result["recommendations"]:
                for item in result["recommendations"]:
                    st.write(f"• {item}")
            else:
                st.write("No recommendations.")

            st.info(f"Saved match result to: {result_path}")