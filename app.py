from pathlib import Path
import tempfile
import json

import pandas as pd
import streamlit as st

from src.ats_score import ATSScorer
from src.parser import extract_text_from_pdf, save_extracted_text
from src.skill_extractor import extract_skills, save_skills, load_skills
from src.matcher import match_resume_to_job, save_match_result
from src.ranking import rank_candidates, save_ranking_results


st.set_page_config(page_title="Resume Screening System", layout="wide")
st.title("Resume Screening System")
st.caption(
    "Upload resumes, extract text, detect skills, compare with a job description, and rank candidates."
)

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []
if "skills_db" not in st.session_state:
    st.session_state.skills_db = load_skills()
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "parsed_resumes" not in st.session_state:
    st.session_state.parsed_resumes = []
if "ranking_results" not in st.session_state:
    st.session_state.ranking_results = []

ats_scorer = ATSScorer()

st.sidebar.header("Project Tools")
st.sidebar.write("Use this app to parse resumes and rank them against a job description.")

tab1, tab2 = st.tabs(["Parse & Skills", "Ranking"])

with tab1:
    uploaded_files = st.file_uploader(
        "Upload resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    col1, col2, col3 = st.columns(3)
    run_parse = col1.button("Parse Resumes", type="primary")
    clear_btn = col3.button("Clear")

    if clear_btn:
        st.session_state.resume_text = ""
        st.session_state.resume_skills = []
        st.session_state.parsed_resumes = []
        st.session_state.ranking_results = []
        st.session_state.job_description = ""
        st.rerun()

    st.subheader("Job Description")
    st.session_state.job_description = st.text_area(
        "Paste the job description below",
        value=st.session_state.job_description,
        height=250,
        placeholder="Paste the job description here...",
    )

    if not uploaded_files:
        st.info("Upload one or more PDF resumes to begin.")
    else:
        st.success(f"Uploaded {len(uploaded_files)} resume(s)")

        if run_parse:
            parsed_resumes = []

            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    tmp_path = tmp.name

                try:
                    text = extract_text_from_pdf(tmp_path)
                    skills_db = st.session_state.skills_db
                    skills = extract_skills(text, skills_db)

                    save_path = save_extracted_text(tmp_path)
                    skills_path = save_skills(uploaded_file.name, skills)

                    parsed_resumes.append(
                        {
                            "name": uploaded_file.name,
                            "text": text,
                            "skills": skills,
                            "save_path": save_path,
                            "skills_path": skills_path,
                        }
                    )
                finally:
                    Path(tmp_path).unlink(missing_ok=True)

            st.session_state.parsed_resumes = parsed_resumes
            st.session_state.resume_text = parsed_resumes[0]["text"] if parsed_resumes else ""
            st.session_state.resume_skills = parsed_resumes[0]["skills"] if parsed_resumes else []

            st.success("Resumes parsed successfully.")

            for resume in parsed_resumes:
                with st.expander(f"Preview: {resume['name']}", expanded=False):
                    text = resume["text"]
                    skills = resume["skills"]

                    st.write(f"Characters extracted: {len(text)}")
                    st.write(f"Words extracted: {len(text.split())}")

                    stat1, stat2, stat3 = st.columns(3)
                    stat1.metric("Skills Detected", len(skills))
                    stat2.metric("Unique Skills", len(set(skills)))
                    stat3.metric("Database Size", len(st.session_state.skills_db))

                    st.text_area("Extracted text", text, height=300)

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
                    for skill in st.session_state.skills_db[:50]:
                        comparison_data.append(
                            {
                                "Skill": skill,
                                "Found": "✅" if skill.lower() in lower_text else "❌",
                            }
                        )

                    st.dataframe(
                        pd.DataFrame(comparison_data),
                        width="stretch",
                        hide_index=True,
                    )

                    st.info(f"Saved extracted text to: {resume['save_path']}")
                    st.info(f"Saved skills to: {resume['skills_path']}")

with tab2:
    st.subheader("Ranking Candidates")

    compare_btn = st.button("Rank Candidates")

    if compare_btn:
        if not st.session_state.parsed_resumes:
            st.warning("Please parse the resumes first.")
        elif not st.session_state.job_description.strip():
            st.warning("Please paste a job description first.")
        else:
            ranked_results = rank_candidates(
                st.session_state.parsed_resumes,
                st.session_state.job_description,
                st.session_state.skills_db,
            )

            st.session_state.ranking_results = ranked_results
            save_path = save_ranking_results(ranked_results)

            st.subheader("🏆 Candidate Rankings")

            if ranked_results:
                ranking_df = pd.DataFrame(
                    [
                        {
                            "Rank": i + 1,
                            "Candidate": item["name"],
                            "ATS Score": item["ats_score"],
                            "Match %": item["match_percent"],
                        }
                        for i, item in enumerate(ranked_results)
                    ]
                )

                st.dataframe(ranking_df, use_container_width=True, hide_index=True)

                best = ranked_results[0]
                st.subheader("⭐ Best Candidate")
                top_col1, top_col2, top_col3 = st.columns(3)
                top_col1.metric("Candidate", best["name"])
                top_col2.metric("ATS Score", best["ats_score"])
                top_col3.metric("Match %", f"{best['match_percent']}%")

                st.success("Recommendation: Highly recommended for interview.")

                st.subheader("Candidate Details")
                for item in ranked_results:
                    with st.expander(f"{item['rank']}. {item['name']}"):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("ATS Score", item["ats_score"])
                        c2.metric("Match %", f"{item['match_percent']}%")
                        c3.metric("Matched Skills", len(item["matched_skills"]))

                        st.write("**Matched Skills:**")
                        st.write(", ".join(item["matched_skills"]) if item["matched_skills"] else "None")

                        st.write("**Missing Skills:**")
                        st.write(", ".join(item["missing_skills"]) if item["missing_skills"] else "None")

                        st.write("**Feedback:**")
                        if item.get("feedback"):
                            for fb in item["feedback"]:
                                st.write(f"• {fb}")
                        else:
                            st.write("No feedback available.")

                        st.write("**Recommendations:**")
                        if item.get("recommendations"):
                            for rec in item["recommendations"]:
                                st.write(f"• {rec}")
                        else:
                            st.write("No recommendations.")

                st.info(f"Saved ranking results to: {save_path}")
            else:
                st.warning("No ranking results were generated.")