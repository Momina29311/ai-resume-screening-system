[1mdiff --git a/README.md b/README.md[m
[1mindex c9fea64..5318556 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -6,9 +6,9 @@[m
 [![Streamlit](https://img.shields.io/badge/streamlit-app-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)[m
 [![Tests](https://img.shields.io/badge/tests-30%20passing-brightgreen.svg)](https://github.com/Momina29311/ai-resume-screening-system)[m
 [m
[31m-ResumeIQ is an end-to-end AI-powered resume screening system that parses resumes, preprocesses text with NLP, extracts technical skills, matches resumes to job descriptions, and predicts a transparent ATS score.[m
[32m+[m[32mResumeIQ is an AI-powered resume screening system that parses resumes, preprocesses text with NLP, extracts skills, matches resumes with job descriptions, and predicts an ATS score using a transparent rule-based engine.[m[41m[m
 [m
[31m-This project is being built publicly as part of my machine learning and data science journey.[m
[32m+[m[32mThis project is being built publicly as part of my machine learning and data science learning journey.[m[41m[m
 [m
 ---[m
 [m
[36m@@ -20,7 +20,7 @@[m [mResumeIQ helps automate early-stage resume screening by combining:[m
 - Skill extraction.[m
 - Resume-to-job matching.[m
 - ATS score prediction.[m
[31m-- Streamlit-based dashboard visualization.[m
[32m+[m[32m- Streamlit dashboard visualization.[m[41m[m
 [m
 It is designed to make resume analysis more structured, explainable, and useful for both candidates and recruiters.[m
 [m
[36m@@ -28,7 +28,7 @@[m [mIt is designed to make resume analysis more structured, explainable, and useful[m
 [m
 ## ✅ What’s Completed[m
 [m
[31m-### Core pipeline[m
[32m+[m[32m### Core Pipeline[m[41m[m
 - ✅ Project planning and architecture.[m
 - ✅ Resume parsing engine.[m
 - ✅ NLP preprocessing pipeline.[m
[36m@@ -36,7 +36,7 @@[m [mIt is designed to make resume analysis more structured, explainable, and useful[m
 - ✅ Resume-to-job matching engine.[m
 - ✅ ATS score prediction engine.[m
 [m
[31m-### Application layer[m
[32m+[m[32m### Application Layer[m[41m[m
 - ✅ Streamlit dashboard integration.[m
 - ✅ Resume upload and parsing.[m
 - ✅ Extracted text preview and download.[m
[36m@@ -71,7 +71,7 @@[m [mThis version introduced the ATS Score Prediction Engine, which evaluates resume[m
 [m
 ResumeIQ now calculates an ATS score using a transparent rule-based system.[m
 [m
[31m-### Scoring categories[m
[32m+[m[32m### Scoring Categories[m[41m[m
 - Skill Match — 40[m
 - Education — 15[m
 - Experience — 20[m
[36m@@ -192,8 +192,8 @@[m [mDashboard + JSON Export[m
 ai-resume-screening-system/[m
 │[m
 ├── app.py[m
[31m-├── requirements.txt[m
 ├── README.md[m
[32m+[m[32m├── requirements.txt[m[41m[m
 │[m
 ├── data/[m
 │   ├── raw/[m
[36m@@ -209,9 +209,8 @@[m [mai-resume-screening-system/[m
 │   ├── ats_score.py[m
 │   └── config.py[m
 │[m
[31m-├── models/[m
[31m-├── notebooks/[m
[31m-└── tests/[m
[32m+[m[32m├── tests/[m[41m[m
[32m+[m[32m└── notebooks/[m[41m[m
 ```[m
 [m
 ---[m
[1mdiff --git a/app.py b/app.py[m
[1mindex 63efe48..a001cb9 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -9,12 +9,13 @@[m [mfrom src.ats_score import ATSScorer[m
 from src.parser import extract_text_from_pdf, save_extracted_text[m
 from src.skill_extractor import extract_skills, save_skills, load_skills[m
 from src.matcher import match_resume_to_job, save_match_result[m
[32m+[m[32mfrom src.ranking import rank_candidates, save_ranking_results[m
 [m
 [m
 st.set_page_config(page_title="Resume Screening System", layout="wide")[m
 st.title("Resume Screening System")[m
[31m-st.write([m
[31m-    "Upload a PDF resume to extract text, detect skills, compare it with a job description, and calculate ATS score."[m
[32m+[m[32mst.caption([m
[32m+[m[32m    "Upload resumes, extract text, detect skills, compare with a job description, and rank candidates."[m
 )[m
 [m
 if "resume_text" not in st.session_state:[m
[36m@@ -25,27 +26,36 @@[m [mif "skills_db" not in st.session_state:[m
     st.session_state.skills_db = load_skills()[m
 if "job_description" not in st.session_state:[m
     st.session_state.job_description = ""[m
[32m+[m[32mif "parsed_resumes" not in st.session_state:[m
[32m+[m[32m    st.session_state.parsed_resumes = [][m
[32m+[m[32mif "ranking_results" not in st.session_state:[m
[32m+[m[32m    st.session_state.ranking_results = [][m
 [m
 ats_scorer = ATSScorer()[m
 [m
[31m-uploaded_file = st.file_uploader("Upload a resume PDF", type=["pdf"])[m
[32m+[m[32mst.sidebar.header("Project Tools")[m
[32m+[m[32mst.sidebar.write("Use this app to parse resumes and rank them against a job description.")[m
 [m
[31m-col1, col2 = st.columns(2)[m
[31m-run_parse = col1.button("Parse Resume", type="primary")[m
[31m-compare_btn = col2.button("Compare Resume")[m
[31m-clear_btn = st.button("Clear")[m
[32m+[m[32mtab1, tab2 = st.tabs(["Parse & Skills", "Ranking"])[m
 [m
[31m-if clear_btn:[m
[31m-    st.session_state.resume_text = ""[m
[31m-    st.session_state.resume_skills = [][m
[31m-    st.session_state.job_description = ""[m
[31m-    st.rerun()[m
[32m+[m[32mwith tab1:[m
[32m+[m[32m    uploaded_files = st.file_uploader([m
[32m+[m[32m        "Upload resume PDFs",[m
[32m+[m[32m        type=["pdf"],[m
[32m+[m[32m        accept_multiple_files=True[m
[32m+[m[32m    )[m
 [m
[31m-if uploaded_file is None:[m
[31m-    st.info("Upload a PDF to begin.")[m
[31m-else:[m
[31m-    st.success(f"Uploaded: {uploaded_file.name}")[m
[31m-    st.write(f"File type: {uploaded_file.type}")[m
[32m+[m[32m    col1, col2, col3 = st.columns(3)[m
[32m+[m[32m    run_parse = col1.button("Parse Resumes", type="primary")[m
[32m+[m[32m    clear_btn = col3.button("Clear")[m
[32m+[m
[32m+[m[32m    if clear_btn:[m
[32m+[m[32m        st.session_state.resume_text = ""[m
[32m+[m[32m        st.session_state.resume_skills = [][m
[32m+[m[32m        st.session_state.parsed_resumes = [][m
[32m+[m[32m        st.session_state.ranking_results = [][m
[32m+[m[32m        st.session_state.job_description = ""[m
[32m+[m[32m        st.rerun()[m
 [m
     st.subheader("Job Description")[m
     st.session_state.job_description = st.text_area([m
[36m@@ -55,155 +65,163 @@[m [melse:[m
         placeholder="Paste the job description here...",[m
     )[m
 [m
[31m-    if run_parse:[m
[31m-        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:[m
[31m-            tmp.write(uploaded_file.getbuffer())[m
[31m-            tmp_path = tmp.name[m
[31m-[m
[31m-        try:[m
[31m-            text = extract_text_from_pdf(tmp_path)[m
[31m-            skills_db = st.session_state.skills_db[m
[31m-            skills = extract_skills(text, skills_db)[m
[31m-[m
[31m-            st.session_state.resume_text = text[m
[31m-            st.session_state.resume_skills = skills[m
[31m-[m
[31m-            save_path = save_extracted_text(tmp_path)[m
[31m-            skills_path = save_skills(uploaded_file.name, skills)[m
[31m-[m
[31m-            st.success("Resume parsed successfully.")[m
[31m-            st.write(f"Characters extracted: {len(text)}")[m
[31m-            st.write(f"Words extracted: {len(text.split())}")[m
[31m-[m
[31m-            stat1, stat2, stat3 = st.columns(3)[m
[31m-            stat1.metric("Skills Detected", len(skills))[m
[31m-            stat2.metric("Unique Skills", len(set(skills)))[m
[31m-            stat3.metric("Database Size", len(skills_db))[m
[31m-[m
[31m-            st.subheader("Preview")[m
[31m-            st.text_area("Extracted text", text, height=400)[m
[31m-[m
[31m-            st.subheader("Detected Skills")[m
[31m-            if skills:[m
[31m-                badge_cols = st.columns(3)[m
[31m-                for i, skill in enumerate(skills):[m
[31m-                    with badge_cols[i % 3]:[m
[31m-                        st.badge(skill, color="blue")[m
[31m-            else:[m
[31m-                st.warning("No skills detected.")[m
[31m-[m
[31m-            st.subheader("Skill Comparison")[m
[31m-            comparison_data = [][m
[31m-            lower_text = text.lower()[m
[31m-            for skill in skills_db[:50]:[m
[31m-                comparison_data.append([m
[31m-                    {[m
[31m-                        "Skill": skill,[m
[31m-                        "Found": "✅" if skill.lower() in lower_text else "❌",[m
[31m-                    }[m
[31m-                )[m
[31m-            st.dataframe([m
[31m-                pd.DataFrame(comparison_data),[m
[31m-                use_container_width=True,[m
[31m-                hide_index=True,[m
[31m-            )[m
[31m-[m
[31m-            st.info(f"Saved extracted text to: {save_path}")[m
[31m-            st.info(f"Saved skills to: {skills_path}")[m
[31m-[m
[31m-            st.download_button([m
[31m-                label="Download extracted text",[m
[31m-                data=text,[m
[31m-                file_name=Path(uploaded_file.name).stem + ".txt",[m
[31m-                mime="text/plain",[m
[31m-            )[m
[31m-        finally:[m
[31m-            Path(tmp_path).unlink(missing_ok=True)[m
[32m+[m[32m    if not uploaded_files:[m
[32m+[m[32m        st.info("Upload one or more PDF resumes to begin.")[m
[32m+[m[32m    else:[m
[32m+[m[32m        st.success(f"Uploaded {len(uploaded_files)} resume(s)")[m
[32m+[m
[32m+[m[32m        if run_parse:[m
[32m+[m[32m            parsed_resumes = [][m
[32m+[m
[32m+[m[32m            for uploaded_file in uploaded_files:[m
[32m+[m[32m                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:[m
[32m+[m[32m                    tmp.write(uploaded_file.getbuffer())[m
[32m+[m[32m                    tmp_path = tmp.name[m
[32m+[m
[32m+[m[32m                try:[m
[32m+[m[32m                    text = extract_text_from_pdf(tmp_path)[m
[32m+[m[32m                    skills_db = st.session_state.skills_db[m
[32m+[m[32m                    skills = extract_skills(text, skills_db)[m
[32m+[m
[32m+[m[32m                    save_path = save_extracted_text(tmp_path)[m
[32m+[m[32m                    skills_path = save_skills(uploaded_file.name, skills)[m
[32m+[m
[32m+[m[32m                    parsed_resumes.append([m
[32m+[m[32m                        {[m
[32m+[m[32m                            "name": uploaded_file.name,[m
[32m+[m[32m                            "text": text,[m
[32m+[m[32m                            "skills": skills,[m
[32m+[m[32m                            "save_path": save_path,[m
[32m+[m[32m                            "skills_path": skills_path,[m
[32m+[m[32m                        }[m
[32m+[m[32m                    )[m
[32m+[m[32m                finally:[m
[32m+[m[32m                    Path(tmp_path).unlink(missing_ok=True)[m
[32m+[m
[32m+[m[32m            st.session_state.parsed_resumes = parsed_resumes[m
[32m+[m[32m            st.session_state.resume_text = parsed_resumes[0]["text"] if parsed_resumes else ""[m
[32m+[m[32m            st.session_state.resume_skills = parsed_resumes[0]["skills"] if parsed_resumes else [][m
[32m+[m
[32m+[m[32m            st.success("Resumes parsed successfully.")[m
[32m+[m
[32m+[m[32m            for resume in parsed_resumes:[m
[32m+[m[32m                with st.expander(f"Preview: {resume['name']}", expanded=False):[m
[32m+[m[32m                    text = resume["text"][m
[32m+[m[32m                    skills = resume["skills"][m
[32m+[m
[32m+[m[32m                    st.write(f"Characters extracted: {len(text)}")[m
[32m+[m[32m                    st.write(f"Words extracted: {len(text.split())}")[m
[32m+[m
[32m+[m[32m                    stat1, stat2, stat3 = st.columns(3)[m
[32m+[m[32m                    stat1.metric("Skills Detected", len(skills))[m
[32m+[m[32m                    stat2.metric("Unique Skills", len(set(skills)))[m
[32m+[m[32m                    stat3.metric("Database Size", len(st.session_state.skills_db))[m
[32m+[m
[32m+[m[32m                    st.text_area("Extracted text", text, height=300)[m
[32m+[m
[32m+[m[32m                    st.subheader("Detected Skills")[m
[32m+[m[32m                    if skills:[m
[32m+[m[32m                        badge_cols = st.columns(3)[m
[32m+[m[32m                        for i, skill in enumerate(skills):[m
[32m+[m[32m                            with badge_cols[i % 3]:[m
[32m+[m[32m                                st.badge(skill, color="blue")[m
[32m+[m[32m                    else:[m
[32m+[m[32m                        st.warning("No skills detected.")[m
[32m+[m
[32m+[m[32m                    st.subheader("Skill Comparison")[m
[32m+[m[32m                    comparison_data = [][m
[32m+[m[32m                    lower_text = text.lower()[m
[32m+[m[32m                    for skill in st.session_state.skills_db[:50]:[m
[32m+[m[32m                        comparison_data.append([m
[32m+[m[32m                            {[m
[32m+[m[32m                                "Skill": skill,[m
[32m+[m[32m                                "Found": "✅" if skill.lower() in lower_text else "❌",[m
[32m+[m[32m                            }[m
[32m+[m[32m                        )[m
[32m+[m
[32m+[m[32m                    st.dataframe([m
[32m+[m[32m                        pd.DataFrame(comparison_data),[m
[32m+[m[32m                        use_container_width=True,[m
[32m+[m[32m                        hide_index=True,[m
[32m+[m[32m                    )[m
[32m+[m
[32m+[m[32m                    st.info(f"Saved extracted text to: {resume['save_path']}")[m
[32m+[m[32m                    st.info(f"Saved skills to: {resume['skills_path']}")[m
[32m+[m
[32m+[m[32mwith tab2:[m
[32m+[m[32m    st.subheader("Ranking Candidates")[m
[32m+[m
[32m+[m[32m    compare_btn = st.button("Rank Candidates")[m
 [m
     if compare_btn:[m
[31m-        if not st.session_state.resume_text:[m
[31m-            st.warning("Please parse the resume first.")[m
[32m+[m[32m        if not st.session_state.parsed_resumes:[m
[32m+[m[32m            st.warning("Please parse the resumes first.")[m
         elif not st.session_state.job_description.strip():[m
             st.warning("Please paste a job description first.")[m
         else:[m
[31m-            resume_skills = st.session_state.resume_skills[m
[31m-            skills_db = st.session_state.skills_db[m
[31m-            job_skills = extract_skills(st.session_state.job_description, skills_db)[m
[31m-[m
[31m-            match_result = match_resume_to_job(resume_skills, job_skills)[m
[31m-            result_path = save_match_result(uploaded_file.name, match_result)[m
[31m-[m
[31m-            parsed_result = {[m
[31m-                "skills": resume_skills,[m
[31m-                "education": [],[m
[31m-                "experience": [],[m
[31m-                "projects": [],[m
[31m-                "certifications": [],[m
[31m-                "sections_present": {[m
[31m-                    "contact_info": True,[m
[31m-                    "summary": True,[m
[31m-                    "skills": True,[m
[31m-                    "education": False,[m
[31m-                    "experience": False,[m
[31m-                },[m
[31m-            }[m
[31m-[m
[31m-            ats_result = ats_scorer.score(parsed_result, match_result)[m
[31m-            ats_data = ats_result.to_dict()[m
[31m-[m
[31m-            scores_dir = Path("data/scores")[m
[31m-            scores_dir.mkdir(parents=True, exist_ok=True)[m
[31m-[m
[31m-            with open(scores_dir / "resume_score.json", "w", encoding="utf-8") as f:[m
[31m-                json.dump(ats_data, f, indent=2)[m
[31m-[m
[31m-            st.subheader("Resume Summary")[m
[31m-            c1, c2, c3, c4 = st.columns(4)[m
[31m-[m
[31m-            c1.metric("Match Score", f"{ats_data['match_score']}%")[m
[31m-            c2.metric("ATS Score", f"{ats_data['ats_score']}/100")[m
[31m-            c3.metric("Skills Found", ats_data["skills_found"])[m
[31m-            c4.metric("Missing Skills", len(ats_data["missing_skills"]))[m
[31m-[m
[31m-            st.subheader("ATS Score Breakdown")[m
[31m-            breakdown = ats_data["breakdown"][m
[31m-[m
[31m-            b1, b2, b3 = st.columns(3)[m
[31m-            with b1:[m
[31m-                st.metric("Skill Match", f"{breakdown['skill_match']}/40")[m
[31m-                st.metric("Projects", f"{breakdown['projects']}/10")[m
[31m-            with b2:[m
[31m-                st.metric("Education", f"{breakdown['education']}/15")[m
[31m-                st.metric("Certifications", f"{breakdown['certifications']}/10")[m
[31m-            with b3:[m
[31m-                st.metric("Experience", f"{breakdown['experience']}/20")[m
[31m-                st.metric("Completeness", f"{breakdown['completeness']}/5")[m
[31m-[m
[31m-            st.subheader("Matched Skills")[m
[31m-            if match_result["matched_skills"]:[m
[31m-                st.write(", ".join(match_result["matched_skills"]))[m
[31m-            else:[m
[31m-                st.write("None")[m
[31m-[m
[31m-            st.subheader("Missing Skills")[m
[31m-            if match_result["missing_skills"]:[m
[31m-                st.write(", ".join(match_result["missing_skills"]))[m
[31m-            else:[m
[31m-                st.write("None")[m
[32m+[m[32m            ranked_results = rank_candidates([m
[32m+[m[32m                st.session_state.parsed_resumes,[m
[32m+[m[32m                st.session_state.job_description,[m
[32m+[m[32m                st.session_state.skills_db,[m
[32m+[m[32m            )[m
 [m
[31m-            st.subheader("Resume Feedback")[m
[31m-            if ats_data["feedback"]:[m
[31m-                for item in ats_data["feedback"]:[m
[31m-                    st.write(f"• {item}")[m
[31m-            else:[m
[31m-                st.write("No feedback available.")[m
[32m+[m[32m            st.session_state.ranking_results = ranked_results[m
[32m+[m[32m            save_path = save_ranking_results(ranked_results)[m
[32m+[m
[32m+[m[32m            st.subheader("🏆 Candidate Rankings")[m
[32m+[m
[32m+[m[32m            if ranked_results:[m
[32m+[m[32m                ranking_df = pd.DataFrame([m
[32m+[m[32m                    [[m
[32m+[m[32m                        {[m
[32m+[m[32m                            "Rank": i + 1,[m
[32m+[m[32m                            "Candidate": item["name"],[m
[32m+[m[32m                            "ATS Score": item["ats_score"],[m
[32m+[m[32m                            "Match %": item["match_percent"],[m
[32m+[m[32m                        }[m
[32m+[m[32m                        for i, item in enumerate(ranked_results)[m
[32m+[m[32m                    ][m
[32m+[m[32m                )[m
 [m
[31m-            st.subheader("Recommendations")[m
[31m-            if ats_data["recommendations"]:[m
[31m-                for item in ats_data["recommendations"]:[m
[31m-                    st.write(f"• {item}")[m
[32m+[m[32m                st.dataframe(ranking_df, use_container_width=True, hide_index=True)[m
[32m+[m
[32m+[m[32m                best = ranked_results[0][m
[32m+[m[32m                st.subheader("⭐ Best Candidate")[m
[32m+[m[32m                top_col1, top_col2, top_col3 = st.columns(3)[m
[32m+[m[32m                top_col1.metric("Candidate", best["name"])[m
[32m+[m[32m                top_col2.metric("ATS Score", best["ats_score"])[m
[32m+[m[32m                top_col3.metric("Match %", f"{best['match_percent']}%")[m
[32m+[m
[32m+[m[32m                st.success("Recommendation: Highly recommended for interview.")[m
[32m+[m
[32m+[m[32m                st.subheader("Candidate Details")[m
[32m+[m[32m                for item in ranked_results:[m
[32m+[m[32m                    with st.expander(f"{item['rank']}. {item['name']}"):[m
[32m+[m[32m                        c1, c2, c3 = st.columns(3)[m
[32m+[m[32m                        c1.metric("ATS Score", item["ats_score"])[m
[32m+[m[32m                        c2.metric("Match %", f"{item['match_percent']}%")[m
[32m+[m[32m                        c3.metric("Matched Skills", len(item["matched_skills"]))[m
[32m+[m
[32m+[m[32m                        st.write("**Matched Skills:**")[m
[32m+[m[32m                        st.write(", ".join(item["matched_skills"]) if item["matched_skills"] else "None")[m
[32m+[m
[32m+[m[32m                        st.write("**Missing Skills:**")[m
[32m+[m[32m                        st.write(", ".join(item["missing_skills"]) if item["missing_skills"] else "None")[m
[32m+[m
[32m+[m[32m                        st.write("**Feedback:**")[m
[32m+[m[32m                        if item.get("feedback"):[m
[32m+[m[32m                            for fb in item["feedback"]:[m
[32m+[m[32m                                st.write(f"• {fb}")[m
[32m+[m[32m                        else:[m
[32m+[m[32m                            st.write("No feedback available.")[m
[32m+[m
[32m+[m[32m                        st.write("**Recommendations:**")[m
[32m+[m[32m                        if item.get("recommendations"):[m
[32m+[m[32m                            for rec in item["recommendations"]:[m
[32m+[m[32m                                st.write(f"• {rec}")[m
[32m+[m[32m                        else:[m
[32m+[m[32m                            st.write("No recommendations.")[m
[32m+[m
[32m+[m[32m                st.info(f"Saved ranking results to: {save_path}")[m
             else:[m
[31m-                st.write("No recommendations.")[m
[31m-[m
[31m-            st.info(f"Saved match result to: {result_path}")[m
[31m-            st.info(f"Saved ATS score to: {scores_dir / 'resume_score.json'}")[m
\ No newline at end of file[m
[32m+[m[32m                st.warning("No ranking results were generated.")[m
\ No newline at end of file[m
