# 🚀 ResumeIQ – AI-Powered Resume Screening System

[![Version](https://img.shields.io/badge/version-v1.2-blue.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Status](https://img.shields.io/badge/status-active%20development-orange.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Python](https://img.shields.io/badge/python-3.14+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-live-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-supported-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-success.svg?logo=githubactions)](https://github.com/Momina29311/ai-resume-screening-system/actions)
[![Tests](https://img.shields.io/badge/tests-46%20automated-brightgreen.svg)](https://github.com/Momina29311/ai-resume-screening-system)

---

# 📄 ResumeIQ

ResumeIQ is an AI-powered Resume Screening System that automates early-stage recruitment by parsing resumes, extracting technical skills, comparing candidates against job descriptions using both keyword and semantic matching, calculating ATS scores, ranking applicants, and presenting recruiter-friendly hiring insights through an interactive dashboard.

The project combines Natural Language Processing (NLP), sentence-embedding-based semantic similarity, rule-based AI, automated testing, Docker containerization, cloud deployment, centralized configuration, logging, and CI/CD to simulate a production-ready AI application.

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

---

## 🧬 Semantic Matching Engine (NEW)

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
| Certifications | 10 |
| Resume Completeness | 5 |

### Output

- ATS Score
- Category Breakdown
- Resume Feedback
- Improvement Suggestions
- JSON Export

---

## 🧮 Final Ranking Score (NEW)

Each candidate now gets a blended **Final Score** in addition to their raw ATS Score:

```
Final Score = (ATS Score × 0.7) + (Semantic Match % × 0.3)
```

Candidate ranking, "Top Candidate" selection, and score-gap calculations are now based on Final Score rather than ATS Score alone.

---

## 🏆 Candidate Ranking

- Upload multiple resumes
- Automatic candidate ranking by Final Score
- Sort by Final Score, ATS Score, Semantic Match, Keyword Match, or Years Experience
- Filter by minimum ATS score and recommendation level
- Top candidate recommendation
- Candidate comparison (ATS Score, Keyword Match, Semantic Match, Final Score, Years Exp.)
- Ranking table
- CSV & JSON export (now includes semantic score and final score)

---

## 📊 Recruiter Hiring Insights

Recruiters can move beyond individual resumes and analyze the entire hiring pipeline.

### Hiring Analytics

- Average ATS Score
- Average Keyword Match %
- Average Semantic Match % (NEW)
- Highest Semantic Match % (NEW)
- Candidate Statistics
- Skill Gap Analysis
- Recommendation Distribution
- ATS Score Distribution

These insights help recruiters quickly understand candidate quality and identify the most common missing skills across applicants.

---

## 🖥 Interactive Recruiter Dashboard

The dashboard provides an end-to-end hiring workflow.

### Dashboard Modules

- Resume Upload
- Resume Parsing
- Skill Analysis
- Job Description Matching (Keyword + Semantic)
- ATS Score Dashboard
- Semantic Match Comparison Chart (NEW)
- Candidate Ranking
- Hiring Insights
- Candidate Comparison
- Feedback & Recommendations
- JSON & CSV Export

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
        Final Score Blending (ATS + Semantic)
                    │
                    ▼
          Candidate Ranking System
                    │
                    ▼
        Recruiter Hiring Insights
                    │
                    ▼
       Interactive Streamlit Dashboard
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     JSON / CSV Export   Live Deployment
                                   │
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
    ├── ranking.py
    └── config.py
```

---

# ✅ Automated Testing

Current automated tests cover:

- Resume Parsing
- Resume Matching (keyword + semantic)
- ATS Score Engine
- Candidate Ranking

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
| **v1.2** | **Semantic Matching Engine + Final Score Blending** | ✅ |

---

# 🚀 Next Roadmap

- Explainable AI (XAI)
- Machine Learning-based ATS Prediction
- OCR for Scanned Resumes
- Resume Embedding Caching for Faster Re-Ranking
- Recruiter Authentication
- REST API
- MLOps Pipeline
- Kubernetes Deployment
- Cloud Database Integration

---

# 👩‍💻 Author

## Momina Zaheer

**Computer Science Student | AI & Data Science Enthusiast**

I'm building AI projects publicly to strengthen my Machine Learning, Data Science, AI Engineering, and Software Engineering skills while documenting the journey one day at a time.

⭐ If you found ResumeIQ useful, consider giving the repository a **star** and sharing your feedback!
