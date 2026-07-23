# 🚀 ResumeIQ – AI-Powered Resume Screening System

[![Version](https://img.shields.io/badge/version-v1.0-blue.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Status](https://img.shields.io/badge/status-active%20development-orange.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Python](https://img.shields.io/badge/python-3.14+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-live-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-supported-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-success.svg?logo=githubactions)](https://github.com/Momina29311/ai-resume-screening-system/actions)
[![Tests](https://img.shields.io/badge/tests-30%20passing-brightgreen.svg)](https://github.com/Momina29311/ai-resume-screening-system)

---

# 📄 ResumeIQ

ResumeIQ is an AI-powered Resume Screening System that automates the early stages of recruitment by parsing resumes, extracting technical skills, comparing candidates against job descriptions, calculating ATS scores, ranking applicants, and providing actionable feedback through an interactive Streamlit dashboard.

The project combines NLP techniques, rule-based intelligence, automated testing, Docker containerization, cloud deployment, and GitHub Actions CI to simulate a production-ready AI application.

Built publicly as part of my Machine Learning & Data Science journey.

---

# 🌐 Live Demo

### 🚀 Streamlit Cloud

https://momina-resumeiq.streamlit.app

---

# ✨ Key Features

## 📄 Resume Parsing
- Upload one or multiple PDF resumes
- Extract resume text
- Resume preview
- Download extracted text
- Character & word statistics

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
- Export extracted skills as JSON

---

## 🔎 Resume Matching
- Compare resumes with job descriptions
- Detect matched skills
- Detect missing skills
- Calculate Match Percentage

---

## ⭐ ATS Score Engine

Transparent rule-based ATS scoring with weighted categories.

### ATS Breakdown

| Category | Weight |
|-----------|---------|
| Skill Match | 40 |
| Experience | 20 |
| Education | 15 |
| Projects | 10 |
| Certifications | 10 |
| Resume Completeness | 5 |

### Output

- Overall ATS Score
- Category-wise Breakdown
- Resume Feedback
- Personalized Recommendations
- JSON Export

---

## 🏆 Candidate Ranking

- Upload multiple resumes
- Rank candidates automatically
- Best candidate recommendation
- Candidate comparison
- Ranking table
- JSON export

---

## 📊 Interactive Dashboard

- Resume Upload
- Job Description Input
- ATS Summary Cards
- Skill Analysis
- Resume Feedback
- Candidate Ranking
- Export Results

---

## ☁ Deployment

- Streamlit Community Cloud
- Docker Container
- Local Development Support

---

## ⚙ CI/CD

GitHub Actions automatically:

- Install dependencies
- Run automated tests
- Verify project builds successfully
- Validate every push to the repository

---

# 📊 Complete Workflow

```text
                 PDF Resume(s)
                       │
                       ▼
              Resume Parsing Engine
                       │
                       ▼
              NLP Preprocessing
                       │
                       ▼
               Skill Extraction
                       │
                       ▼
            Resume ↔ Job Matching
                       │
                       ▼
             ATS Score Calculation
                       │
                       ▼
             Candidate Ranking
                       │
                       ▼
          Feedback & Recommendations
                       │
                       ▼
             Interactive Dashboard
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
     JSON Export          Streamlit Deployment
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

### PDF Processing
- pdfplumber

### Web Framework
- Streamlit

### Testing
- pytest

### Deployment
- Streamlit Community Cloud
- Docker

### DevOps
- GitHub Actions
- GitHub CI

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
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── sample_resumes/
│   └── scores/
│
├── outputs/
│
├── src/
│   ├── parser.py
│   ├── preprocessing.py
│   ├── skill_extractor.py
│   ├── matcher.py
│   ├── ats_score.py
│   ├── ranking.py
│   └── config.py
│
├── tests/
└── notebooks/
```

---

# ✅ Testing

Current automated testing includes:

- Resume Parser
- Resume Matcher
- ATS Score Engine
- Candidate Ranking

✅ 30 Automated Tests Passing

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

## Run Application

```bash
streamlit run app.py
```

---

# 🐳 Docker

## Build

```bash
docker build -t resumeiq .
```

## Run

```bash
docker run -p 8501:8501 resumeiq
```

Visit:

```
http://localhost:8501
```

---

# 📅 Development Timeline

| Version | Milestone | Status |
|----------|-----------|--------|
| v0.1 | Project Planning | ✅ |
| v0.2 | Resume Parsing Engine | ✅ |
| v0.3 | NLP Preprocessing | ✅ |
| v0.4 | Skill Extraction | ✅ |
| v0.5 | Resume Matching | ✅ |
| v0.6 | ATS Score Engine | ✅ |
| v0.7 | Candidate Ranking | ✅ |
| v0.8 | Streamlit Cloud Deployment | ✅ |
| v0.9 | Docker Containerization | ✅ |
| v1.0 | GitHub Actions CI | ✅ |

---

# 🚀 What's Next?

- Explainable AI (XAI)
- Machine Learning–based ATS Prediction
- Semantic Skill Matching
- OCR Support for Scanned Resumes
- Recruiter Dashboard
- Authentication
- REST API
- MLOps Pipeline
- Kubernetes Deployment
- Cloud Database Integration

---

# 👩‍💻 Author

## Momina Zaheer

**Computer Science Student | AI & Data Science Enthusiast**

I'm building AI projects publicly to strengthen my Machine Learning, Data Science, and Software Engineering skills while documenting the journey one day at a time.

If you found this project useful, consider giving it a ⭐ and sharing your feedback!