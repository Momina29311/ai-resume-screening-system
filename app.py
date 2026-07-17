from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from src.parser import extract_text_from_pdf, save_extracted_text
from src.skill_extractor import extract_skills, save_skills, load_skills


st.set_page_config(page_title="Resume Screening System", layout="wide")
st.title("Resume Screening System")
st.write("Upload a PDF resume to extract text, detect skills, and save structured output.")

uploaded_file = st.file_uploader("Upload a resume PDF", type=["pdf"])

col1, col2 = st.columns(2)
run_parse = col1.button("Parse Resume", type="primary")
clear_btn = col2.button("Clear")

if clear_btn:
    st.rerun()

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File type: {uploaded_file.type}")

    if run_parse:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            text = extract_text_from_pdf(tmp_path)
            save_path = save_extracted_text(tmp_path)

            skills_db = load_skills()
            skills = extract_skills(text, skills_db)
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
else:
    st.info("Upload a PDF to begin.")