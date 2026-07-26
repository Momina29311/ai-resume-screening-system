from pathlib import Path
import tempfile
import json

import pandas as pd
import streamlit as st

from src.ats_score import ATSScorer
from src.parser import extract_text_from_pdf, save_extracted_text
from src.skill_extractor import extract_skills, save_skills, load_skills
from src.matcher import match_resume_to_job, save_match_result
from src.ranking import (
    rank_candidates,
    save_ranking_results,
    compute_aggregate_insights,
    export_ranking_csv,
)

st.set_page_config(page_title="ResumeIQ", page_icon="🚀", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top left, rgba(255, 87, 87, 0.12), transparent 28%),
            radial-gradient(circle at top right, rgba(88, 166, 255, 0.10), transparent 24%),
            linear-gradient(135deg, #090b12 0%, #0f1220 45%, #090b12 100%);
        color: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b1d2a 0%, #121420 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .main-title {
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #ffffff, #ff6b6b, #ffd93d, #4d96ff, #ffffff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 7s ease infinite;
        margin-top: 0.2rem;
        margin-bottom: 0.35rem;
    }

    .subtitle {
        color: #a7afc4;
        font-size: 1rem;
        margin-bottom: 1.3rem;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .glass-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
        backdrop-filter: blur(10px);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 36px rgba(0,0,0,0.28);
        border-color: rgba(255,255,255,0.16);
    }

    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(255,107,107,0.18), rgba(77,150,255,0.18));
        border: 1px solid rgba(255,255,255,0.09);
        color: #e8ecff;
        font-size: 0.88rem;
        animation: pulseGlow 2.2s infinite;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(77,150,255,0.22); }
        70% { box-shadow: 0 0 0 14px rgba(77,150,255,0); }
        100% { box-shadow: 0 0 0 0 rgba(77,150,255,0); }
    }

    .recommend-good {
        background: linear-gradient(90deg, rgba(46,204,113,0.20), rgba(39,174,96,0.12));
        border: 1px solid rgba(46,204,113,0.35);
        color: #b7ffca;
        border-radius: 16px;
        padding: 0.9rem 1rem;
    }

    .recommend-mid {
        background: linear-gradient(90deg, rgba(241,196,15,0.18), rgba(243,156,18,0.10));
        border: 1px solid rgba(241,196,15,0.28);
        color: #ffe7a0;
        border-radius: 16px;
        padding: 0.9rem 1rem;
    }

    .recommend-bad {
        background: linear-gradient(90deg, rgba(231,76,60,0.18), rgba(192,57,43,0.10));
        border: 1px solid rgba(231,76,60,0.30);
        color: #ffb0aa;
        border-radius: 16px;
        padding: 0.9rem 1rem;
    }

    .tip-carousel {
        position: relative;
        height: 2.6rem;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1.1rem;
        padding: 0 1.1rem;
    }

    .tip-carousel .tip-slide {
        position: absolute;
        left: 1.1rem;
        right: 1.1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #c7cee6;
        font-size: 0.92rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        opacity: 0;
        animation: tipCycle 16s infinite;
    }

    .tip-carousel .tip-slide:nth-child(1) { animation-delay: 0s; }
    .tip-carousel .tip-slide:nth-child(2) { animation-delay: 4s; }
    .tip-carousel .tip-slide:nth-child(3) { animation-delay: 8s; }
    .tip-carousel .tip-slide:nth-child(4) { animation-delay: 12s; }

    @keyframes tipCycle {
        0% { opacity: 0; transform: translate(12px, -50%); }
        3% { opacity: 1; transform: translate(0, -50%); }
        22% { opacity: 1; transform: translate(0, -50%); }
        25% { opacity: 0; transform: translate(-12px, -50%); }
        100% { opacity: 0; }
    }

    .insight-pill {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        margin: 0.15rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #e8ecff;
        font-size: 0.85rem;
    }

    .animate-in {
        animation: fadeUp 0.5s ease both;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
    }

    div[data-testid="stButton"] > button {
        border-radius: 12px;
        transition: all 0.25s ease;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.22);
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 0.75rem 0.8rem;
        box-shadow: 0 8px 18px rgba(0,0,0,0.14);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="hero-badge">AI Recruiter Dashboard • ResumeIQ</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Resume Screening System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload resumes, extract skills, compare with a job description, and rank candidates with an explainable ATS profile.</div>',
    unsafe_allow_html=True,
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
if "loading" not in st.session_state:
    st.session_state.loading = False

ats_scorer = ATSScorer()

st.sidebar.header("Project Tools")
st.sidebar.write("Use this app to parse resumes and rank them against a job description.")
if st.session_state.parsed_resumes:
    st.sidebar.metric("Resumes Parsed", len(st.session_state.parsed_resumes))
if st.session_state.ranking_results:
    insights = compute_aggregate_insights(st.session_state.ranking_results)
    st.sidebar.metric("Avg ATS Score", insights["avg_ats_score"])
    st.sidebar.metric("Avg Match %", f"{insights['avg_match_percent']}%")

tab1, tab2, tab3 = st.tabs(["Parse & Skills", "Ranking", "Insights"])

with tab1:
    _tips = [
        "💡 Upload multiple PDF resumes at once to screen your whole pipeline in one go.",
        "🎯 Add a \"Preferred\" section to your job description so required vs. nice-to-have skills are weighted correctly.",
        "📊 Head to the Insights tab after ranking to see the most common skill gaps across candidates.",
        "🔍 Use the Compare tool in the Ranking tab to put two finalists side-by-side.",
    ]
    _slide_html = "".join(f'<div class="tip-slide">{tip}</div>' for tip in _tips)
    st.markdown(f'<div class="tip-carousel">{_slide_html}</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload resume PDFs",
        type=["pdf"],
        accept_multiple_files=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])
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
        placeholder="Paste the job description here... Tip: add a 'Preferred' section to separate must-have vs nice-to-have skills.",
    )

    if not uploaded_files:
        st.info("Upload one or more PDF resumes to begin.")
    else:
        st.success(f"Uploaded {len(uploaded_files)} resume(s)")

        if run_parse:
            st.session_state.loading = True
            parsed_resumes = []
            progress = st.progress(0)

            for idx, uploaded_file in enumerate(uploaded_files, start=1):
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

                progress.progress(idx / len(uploaded_files))

            st.session_state.parsed_resumes = parsed_resumes
            st.session_state.resume_text = parsed_resumes[0]["text"] if parsed_resumes else ""
            st.session_state.resume_skills = parsed_resumes[0]["skills"] if parsed_resumes else []
            st.session_state.ranking_results = []
            st.session_state.loading = False
            st.success("Resumes parsed successfully.")

        for resume in st.session_state.parsed_resumes:
            with st.expander(f"Preview: {resume['name']}", expanded=False):
                text = resume["text"]
                skills = resume["skills"]

                stat1, stat2, stat3 = st.columns(3)
                stat1.metric("Skills Detected", len(skills))
                stat2.metric("Unique Skills", len(set(skills)))
                stat3.metric("Database Size", len(st.session_state.skills_db))

                st.text_area("Extracted text", text, height=260, key=f"text_{resume['name']}")

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
                    use_container_width=True,
                    hide_index=True,
                )

                st.info(f"Saved extracted text to: {resume['save_path']}")
                st.info(f"Saved skills to: {resume['skills_path']}")

with tab2:
    st.subheader("Ranking Candidates")

    compare_btn = st.button("Rank Candidates")
    json_path = None
    csv_path = None

    if compare_btn:
        if not st.session_state.parsed_resumes:
            st.warning("Please parse the resumes first.")
        elif not st.session_state.job_description.strip():
            st.warning("Please paste a job description first.")
        else:
            st.session_state.loading = True
            with st.spinner("Ranking candidates..."):
                ranked_results = rank_candidates(
                    st.session_state.parsed_resumes,
                    st.session_state.job_description,
                    st.session_state.skills_db,
                )
            st.session_state.ranking_results = ranked_results
            json_path = save_ranking_results(ranked_results)
            csv_path = export_ranking_csv(ranked_results)
            st.session_state.loading = False

    ranked_results = st.session_state.ranking_results
    visible_results = []

    if ranked_results:
        filt_col1, filt_col2, filt_col3 = st.columns([2, 1, 1])
        min_score = filt_col1.slider("Minimum ATS score", 0, 100, 0)
        rec_filter = filt_col2.multiselect(
            "Recommendation",
            options=["Highly Recommended", "Consider", "Not Recommended"],
            default=[],
        )
        sort_by = filt_col3.selectbox(
            "Sort by",
            ["Final Score", "ATS Score", "Semantic Match", "Keyword Match", "Years Experience"],
        )

        visible_results = [r for r in ranked_results if r["ats_score"] >= min_score]
        if rec_filter:
            visible_results = [r for r in visible_results if r["recommendation_level"] in rec_filter]

        sort_key_map = {
            "Final Score": "final_score",
            "ATS Score": "ats_score",
            "Semantic Match": "semantic_match_percent",
            "Keyword Match": "match_percent",
            "Years Experience": "years_experience",
        }
        visible_results = sorted(
            visible_results,
            key=lambda x: x.get(sort_key_map[sort_by], 0),
            reverse=True,
        )

        st.subheader("🏆 Candidate Rankings")
        ranking_df = pd.DataFrame(
            [
                {
                    "Rank": i + 1,
                    "Candidate": item["name"],
                    "ATS Score": item["ats_score"],
                    "Match %": item["match_percent"],
                    "Semantic %": item.get("semantic_match_percent", 0),
                    "Final Score": item.get("final_score", item["ats_score"]),
                    "Years Exp.": item.get("years_experience", 0),
                    "Recommendation": item["recommendation_level"],
                }
                for i, item in enumerate(visible_results)
            ]
        )
        st.dataframe(ranking_df, use_container_width=True, hide_index=True)

        st.markdown("**ATS Score Comparison**")
        if visible_results:
            ats_chart_df = pd.DataFrame(
                [(item["name"], item["ats_score"]) for item in visible_results],
                columns=["Candidate", "ATS Score"],
            ).set_index("Candidate")
            st.bar_chart(ats_chart_df)

        st.markdown("**Semantic Match Comparison**")
        if visible_results:
            semantic_chart_df = pd.DataFrame(
                [(item["name"], item.get("semantic_match_percent", 0)) for item in visible_results],
                columns=["Candidate", "Semantic Match"],
            ).set_index("Candidate")

            if len(visible_results) >= 2:
                st.bar_chart(semantic_chart_df)
            else:
                st.dataframe(semantic_chart_df, use_container_width=True)

            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    "⬇️ Download JSON",
                    data=json.dumps(ranked_results, indent=2),
                    file_name="ranking_results.json",
                    mime="application/json",
                )
            with dl_col2:
                csv_df = pd.DataFrame(
                    [
                        {
                            "Rank": item["rank"],
                            "Candidate": item["name"],
                            "ATS Score": item["ats_score"],
                            "Match %": item["match_percent"],
                            "Semantic Match": item.get("semantic_match_percent", 0),
                            "Final Score": item.get("final_score", item["ats_score"]),
                            "Years Exp.": item.get("years_experience", 0),
                            "Recommendation": item["recommendation_level"],
                            "Matched Skills": "; ".join(item.get("matched_skills", [])),
                            "Missing Required": "; ".join(item.get("missing_required_skills", [])),
                        }
                        for item in ranked_results
                    ]
                )
                st.download_button(
                    "⬇️ Download CSV",
                    data=csv_df.to_csv(index=False),
                    file_name="ranking_results.csv",
                    mime="text/csv",
                )

        if not visible_results:
            st.info("No candidates match the current filters.")
        else:
            best = visible_results[0]
            st.subheader("⭐ Top Candidate")
            top_col1, top_col2, top_col3, top_col4, top_col5 = st.columns(5)
            top_col1.metric("Candidate", best["name"])
            top_col2.metric("ATS Score", best["ats_score"])
            top_col3.metric("Semantic Match", f"{best.get('semantic_match_percent', 0)}%")
            top_col4.metric("Final Score", best.get("final_score", best["ats_score"]))
            top_col5.metric("Years Exp.", best.get("years_experience", 0))

            rec_level = best.get("recommendation_level", "Recommended")
            feedback = " ".join(best.get("feedback", [])) if isinstance(best.get("feedback"), list) else best.get("feedback", "")

            if rec_level == "Highly Recommended":
                st.markdown(f'<div class="recommend-good"><b>🟢 {rec_level}</b><br>{feedback}</div>', unsafe_allow_html=True)
            elif rec_level == "Consider":
                st.markdown(f'<div class="recommend-mid"><b>🟡 {rec_level}</b><br>{feedback}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="recommend-bad"><b>🔴 {rec_level}</b><br>{feedback}</div>', unsafe_allow_html=True)

            st.subheader("Candidate Details")
            for item in visible_results:
                with st.expander(f"{item['rank']}. {item['name']} — {item['ats_score']} pts", expanded=False):
                    c1, c2, c3, c4, c5 = st.columns(5)
                    c1.metric("ATS Score", item.get("ats_score", 0))
                    c2.metric("Keyword Match", f"{item.get('match_percent', 0)}%")
                    c3.metric("Semantic Match", f"{item.get('semantic_match_percent', 0)}%")
                    c4.metric("Final Score", item.get("final_score", item.get("ats_score", 0)))
                    c5.metric("Matched Skills", len(item.get("matched_skills", [])))

                    sub_overview, sub_skills, sub_feedback = st.tabs(["Overview", "Skills", "Feedback"])

                    with sub_overview:
                        breakdown = item.get("ats_breakdown", {})
                        if breakdown:
                            breakdown_df = pd.DataFrame(
                                [
                                    {"Category": k.replace("_", " ").title(), "Score": v}
                                    for k, v in breakdown.items()
                                    if k != "total"
                                ]
                            ).set_index("Category")
                            st.bar_chart(breakdown_df)
                            st.metric("Total ATS", breakdown.get("total", item.get("ats_score", 0)))

                    with sub_skills:
                        st.write("**Matched Skills:**")
                        matched = item.get("matched_skills", [])
                        if matched:
                            cols = st.columns(3)
                            for i, skill in enumerate(matched):
                                with cols[i % 3]:
                                    st.badge(skill, color="green")
                        else:
                            st.write("None")

                        st.write("**Missing Required Skills:**")
                        missing_req = item.get("missing_required_skills", item.get("missing_skills", []))
                        if missing_req:
                            cols = st.columns(3)
                            for i, skill in enumerate(missing_req):
                                with cols[i % 3]:
                                    st.badge(skill, color="red")
                        else:
                            st.write("None")

                        missing_pref = item.get("missing_preferred_skills", [])
                        if missing_pref:
                            st.write("**Missing Preferred Skills:**")
                            cols = st.columns(3)
                            for i, skill in enumerate(missing_pref):
                                with cols[i % 3]:
                                    st.badge(skill, color="orange")

                    with sub_feedback:
                        st.write("**Feedback:**")
                        fb = item.get("feedback", [])
                        if isinstance(fb, list) and fb:
                            for line in fb:
                                st.write(f"• {line}")
                        elif fb:
                            st.write(fb)
                        else:
                            st.write("No feedback available.")

                        st.write("**Recommendations:**")
                        recs = item.get("recommendations", [])
                        if isinstance(recs, list) and recs:
                            for rec in recs:
                                st.write(f"• {rec}")
                        elif recs:
                            st.write(recs)
                        else:
                            st.write("No recommendations.")

            st.subheader("🔍 Compare Two Candidates")
            names = [r["name"] for r in ranked_results]
            if len(names) >= 2:
                cmp_col1, cmp_col2 = st.columns(2)
                cand_a = cmp_col1.selectbox("Candidate A", names, index=0, key="compare_candidate_a")
                cand_b = cmp_col2.selectbox("Candidate B", names, index=1 if len(names) > 1 else 0, key="compare_candidate_b")

                item_a = next(r for r in ranked_results if r["name"] == cand_a)
                item_b = next(r for r in ranked_results if r["name"] == cand_b)

                compare_df = pd.DataFrame(
                    {
                        "Metric": [
                            "ATS Score",
                            "Keyword Match",
                            "Semantic Match",
                            "Final Score",
                            "Years Exp.",
                        ],
                        cand_a: [
                            item_a.get("ats_score", 0),
                            item_a.get("match_percent", 0),
                            item_a.get("semantic_match_percent", 0),
                            item_a.get("final_score", item_a.get("ats_score", 0)),
                            item_a.get("years_experience", 0),
                        ],
                        cand_b: [
                            item_b.get("ats_score", 0),
                            item_b.get("match_percent", 0),
                            item_b.get("semantic_match_percent", 0),
                            item_b.get("final_score", item_b.get("ats_score", 0)),
                            item_b.get("years_experience", 0),
                        ],
                    }
                ).set_index("Metric")
                st.dataframe(compare_df, use_container_width=True)
            else:
                st.info("Need at least two candidates to compare.")

        if json_path:
            st.info(f"Saved ranking results to: {json_path}")
        if csv_path:
            st.info(f"Saved CSV results to: {csv_path}")
    else:
        st.info("Run ranking to see the candidate leaderboard here.")

with tab3:
    st.subheader("📊 Hiring Insights")

    if not st.session_state.ranking_results:
        st.info("Rank candidates in the Ranking tab to unlock insights.")
    else:
        insights = compute_aggregate_insights(st.session_state.ranking_results)
        i1, i2, i3, i4, i5 = st.columns(5)
        i1.metric("Candidates Ranked", insights["candidate_count"])
        i2.metric("Average ATS Score", insights["avg_ats_score"])
        i3.metric("Average Keyword Match", f"{insights['avg_match_percent']}%")
        i4.metric("Average Semantic Match", f"{insights.get('avg_semantic_match_percent', 0)}%")
        i5.metric("Highest Semantic Match", f"{insights.get('highest_semantic_match_percent', 0)}%")

        st.markdown("**Most Common Skill Gaps Across Candidates**")
        if insights["top_missing_skills"]:
            gap_df = pd.DataFrame(
                insights["top_missing_skills"], columns=["Skill", "Candidates Missing It"]
            ).set_index("Skill")
            st.bar_chart(gap_df)
            st.caption("Consider whether these skills are truly required, or adjust sourcing to target them.")
        else:
            st.write("No significant skill gaps detected — great candidate pool fit!")

        st.markdown("**Recommendation Mix**")
        rec_counts = pd.Series(
            [r["recommendation_level"] for r in st.session_state.ranking_results]
        ).value_counts()
        st.bar_chart(rec_counts)

        st.markdown("**Score Distribution**")
        dist_df = pd.DataFrame(
            {r["name"]: r["ats_score"] for r in st.session_state.ranking_results}.items(),
            columns=["Candidate", "ATS Score"],
        ).set_index("Candidate")
        st.bar_chart(dist_df)