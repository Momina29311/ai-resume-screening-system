# 🚀 ResumeIQ – AI-Powered Resume Screening System

[![Version](https://img.shields.io/badge/version-v1.4-blue.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Status](https://img.shields.io/badge/status-active%20development-orange.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Python](https://img.shields.io/badge/python-3.14+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-live-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-supported-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-success.svg?logo=githubactions)](https://github.com/Momina29311/ai-resume-screening-system/actions)
[![Tests](https://img.shields.io/badge/tests-46%20automated-brightgreen.svg)](https://github.com/Momina29311/ai-resume-screening-system)

---

# 📄 ResumeIQ

ResumeIQ is an AI-powered Resume Screening System that automates early-stage recruitment by parsing resumes, extracting technical skills, comparing candidates against job descriptions using both keyword and semantic matching, calculating ATS scores, ranking applicants with a hybrid AI score, and explaining every ranking decision through an interactive, transparent recruiter dashboard.

The project combines Natural Language Processing (NLP), sentence-embedding-based semantic similarity, rule-based AI, explainable AI (XAI) reasoning, automated testing, Docker containerization, cloud deployment, centralized configuration, logging, and CI/CD to simulate a production-ready AI application.

Built publicly as part of my Machine Learning & AI Engineering journey.

---

# 🌐 Live Demo

### 🚀 Streamlit Cloud

https://momina-resumeiq.streamlit.app

---

# ✨ Core Features

## 📄 Resume Parsing

- Upload one or multiple PDF resumes
- Resume text extraction
- Resume preview
- Character & word statistics
- Download extracted text

---

## 🧠 NLP Preprocessing

- Text cleaning
- Normalization
- Token preparation
- Ready for downstream analysis

---

## 🎯 Skill Extraction

- Detect technical skills
- Skill badge visualization
- Skill comparison against database
- JSON export

---

## 🔎 Resume ↔ Job Matching

- Compare resumes against job descriptions
- Identify matched skills
- Identify missing skills
- Calculate keyword Match Percentage
- Required vs. Preferred skill parsing from job descriptions

---

## 🧬 Semantic Matching Engine

Goes beyond keyword overlap to understand meaning and context.

- Sentence-embedding similarity between full resume text and job description (`sentence-transformers`, `all-MiniLM-L6-v2`)
- Cosine similarity converted into a 0–100 **Semantic Match %**
- Human-readable match labels: Strong / Moderate / Weak Semantic Match
- Blended into scoring so conceptually strong candidates aren't penalized for wording differences alone

---

## ⭐ ATS Score Engine

Transparent rule-based ATS scoring with explainable weighted categories.

### ATS Categories

| Category | Weight |
|-----------|---------|
| Skill Match | 40 |
| Experience | 20 |
| Education | 15 |
| Projects | 10 |
| Certifications | 8 |
| Resume Completeness | 7 |

### Output

- ATS Score
- Category Breakdown
- Resume Feedback
- Improvement Suggestions
- JSON Export

---

## 🧮 Hybrid AI Ranking Score

Each candidate gets a blended **Final Score** that combines rule-based scoring, conceptual fit, and career depth — not ATS alone.

```
Final Score = (ATS Score × 0.60) + (Semantic Match % × 0.30) + (Experience Score × 0.10)
```

- **Experience Score** is a 0–100 normalization of detected years of experience, extracted two ways: explicit phrasing ("5 years of experience") and computed career span from job-history date ranges (e.g. "Mar 2022 – Present"), taking whichever detection yields more credit.
- Candidate ranking, "Top Candidate" selection, and score-gap calculations are based on Final Score rather than raw ATS Score.

---

## 🧠 Explainable AI (XAI)

ResumeIQ doesn't just say *"ATS Score: 89"* — it explains **why** a candidate ranked where they did, turning the ranking engine from a black box into a transparent, audit-friendly system.

### XAI Capabilities

- **AI Decision Explanations** — plain-language reasoning for every ranked candidate, generated relative to the rest of the pool (e.g. "High ATS score", "Strong semantic similarity", "Few missing skills")
- **Score Contribution Breakdown** — the Final Score shown as a transparent calculation:
  ```
  ATS Score Contribution     : 70 × 0.60 = 42.0
  Semantic Similarity        : 92 × 0.30 = 27.6
  Experience Bonus           : 100 × 0.10 = 10.0
  Final Score                : 79.6
  ```
- **Strengths & Weaknesses** — automatically generated per candidate, separate from raw feedback, rendered as scannable pills on the dashboard
- **Recommendation Reasoning** — recommendation labels ("Highly Recommended", "Consider", "Not Recommended") now carry structured, supporting reasons instead of a bare tag
- **Candidate Comparison Explanation** — head-to-head comparisons show *why* one candidate ranks above another (e.g. "Ali ranks higher because: + Better semantic similarity, + More experience, + More required skills matched")
- **Recruiter Insights Upgrade** — Top strengths across the whole candidate pool, most common missing skills, and best overall candidate, surfaced on the Insights dashboard
- **Explainability Report Export** — downloadable JSON and CSV reports containing score breakdowns, strengths, weaknesses, and recommendation reasoning for every candidate, separate from the raw ranking export

---

## 🏆 Candidate Ranking

- Upload multiple resumes
- Automatic candidate ranking by Final Score (Hybrid AI Score)
- Sort by Final Score, ATS Score, Semantic Match, Keyword Match, or Years Experience
- Filter by minimum ATS score and recommendation level
- Top candidate recommendation with explainable reasoning
- Candidate comparison (ATS Score, Keyword Match, Semantic Match, Final Score, Years Exp.) with head-to-head XAI reasoning
- Ranking table
- CSV & JSON export (includes semantic score, experience score, and final score)
- Explainability report export (JSON & CSV)

---

## 📊 Recruiter Hiring Insights

Recruiters can move beyond individual resumes and analyze the entire hiring pipeline.

### Hiring Analytics

- Average ATS Score
- Average Keyword Match %
- Average Semantic Match %
- Highest Semantic Match %
- Average / Highest Final Score
- Best Overall Candidate (NEW)
- Top Strengths Across Candidates (NEW)
- Candidate Statistics
- Skill Gap Analysis
- Recommendation Distribution
- ATS Score Distribution

These insights help recruiters quickly understand candidate quality and identify the most common missing skills and strengths across applicants.

---

## 🖥 Interactive Recruiter Dashboard

The dashboard provides an end-to-end hiring workflow.

### Dashboard Modules

- Resume Upload
- Resume Parsing
- Skill Analysis
- Job Description Matching (Keyword + Semantic)
- ATS Score Dashboard
- Semantic Match Comparison Chart
- Hybrid AI Candidate Ranking
- Explainability Panel per Candidate (NEW)
- Hiring Insights
- Candidate Comparison with XAI Reasoning (NEW)
- Feedback & Recommendations
- JSON & CSV Export (Ranking + Explainability Reports)

---

## ⚙ Configuration & Logging

ResumeIQ includes centralized configuration and application-wide logging.

- Centralized configuration (`config.py`)
- Configurable ATS weights
- Environment-ready settings
- Structured logging
- Easier debugging
- Cleaner architecture

---

## ☁ Deployment

- Streamlit Community Cloud
- Docker Container
- Local Development

---

## ⚙ CI/CD

GitHub Actions automatically:

- Install dependencies
- Run automated tests
- Validate builds
- Verify every push

---

# 📊 Complete ResumeIQ Workflow

```text
             PDF Resume(s)
                    │
                    ▼
          Resume Parsing Engine
                    │
                    ▼
         NLP Preprocessing Layer
                    │
                    ▼
           Skill Extraction Engine
                    │
                    ▼
        Resume ↔ Job Description Matching
             (Keyword + Semantic)
                    │
                    ▼
         Explainable ATS Score Engine
                    │
                    ▼
   Hybrid Final Score (ATS + Semantic + Experience)
                    │
                    ▼
          Candidate Ranking System
                    │
                    ▼
        Explainable AI (XAI) Layer
     (Score Breakdown, Strengths/Weaknesses,
      Recommendation Reasoning, Comparisons)
                    │
                    ▼
        Recruiter Hiring Insights
                    │
                    ▼
       Interactive Streamlit Dashboard
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
 Ranking + Explainability   Live Deployment
      JSON / CSV Export             │
                                     ▼
                            Docker Container
                                     │
                                     ▼
                             GitHub Actions CI
```

---

# 🛠 Tech Stack

### Programming

- Python

### NLP

- NLTK
- sentence-transformers (`all-MiniLM-L6-v2`)

### PDF Processing

- pdfplumber
- pypdf

### Dashboard

- Streamlit

### Data Processing

- Pandas

### Testing

- Pytest

### Deployment

- Streamlit Community Cloud
- Docker

### DevOps

- GitHub Actions
- CI/CD

### Version Control

- Git
- GitHub

---

# 📂 Project Structure

```text
ai-resume-screening-system/

├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app.py
├── config.py
├── Dockerfile
├── README.md
├── requirements.txt
│
├── data/
├── docs/
├── logs/
├── notebooks/
├── outputs/
├── tests/
│
└── src/
    ├── parser.py
    ├── preprocessing.py
    ├── skill_extractor.py
    ├── matcher.py
    ├── semantic_matcher.py
    ├── ats_score.py
    ├── ranking.py          # Hybrid scoring + Explainable AI (XAI) engine
    └── config.py
```

---

# ✅ Automated Testing

Current automated tests cover:

- Resume Parsing
- Resume Matching (keyword + semantic)
- ATS Score Engine
- Candidate Ranking (hybrid scoring)

✅ **46 Automated Tests** — run on every push via GitHub Actions CI

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/Momina29311/ai-resume-screening-system.git
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run ResumeIQ

```bash
streamlit run app.py
```

---

# 🐳 Docker

Build Image

```bash
docker build -t resumeiq .
```

Run Container

```bash
docker run -p 8501:8501 resumeiq
```

Visit

```
http://localhost:8501
```

---

# 📅 Development Timeline

| Version | Milestone | Status |
|----------|-----------|--------|
| v0.1 | Project Planning | ✅ |
| v0.2 | Resume Parsing | ✅ |
| v0.3 | NLP Preprocessing | ✅ |
| v0.4 | Skill Extraction | ✅ |
| v0.5 | Resume Matching | ✅ |
| v0.6 | ATS Score Engine | ✅ |
| v0.7 | Candidate Ranking | ✅ |
| v0.8 | Streamlit Deployment | ✅ |
| v0.9 | Docker Support | ✅ |
| v1.0 | GitHub Actions CI + Configuration & Logging | ✅ |
| v1.1 | Recruiter Hiring Insights Dashboard | ✅ |
| v1.2 | Semantic Matching Engine + Score Blending | ✅ |
| v1.3 | Hybrid AI Candidate Ranking (ATS + Semantic + Experience) | ✅ |
| **v1.4** | **Explainable AI (XAI) for Candidate Ranking** | ✅ |

---

# 🚀 Next Roadmap

- LLM-powered Resume Feedback (personalized improvement suggestions)
- Resume Summarization using an LLM
- OCR for Scanned Resumes
- Machine Learning-based ATS Prediction
- Resume Embedding Caching for Faster Re-Ranking
- Recruiter Authentication & Candidate History
- REST API with FastAPI
- MLOps Pipeline
- Kubernetes Deployment
- Cloud Database Integration

---

# 👩‍💻 Author

## Momina Zaheer

**Computer Science Student | AI & Data Science Enthusiast**

I'm building AI projects publicly to strengthen my Machine Learning, Data Science, AI Engineering, and Software Engineering skills while documenting the journey one day at a time.

⭐ If you found ResumeIQ useful, consider giving the repository a **star** and sharing your feedback!
