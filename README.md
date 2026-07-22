# 🚀 ResumeIQ – AI-Powered Resume Screening System

[![Version](https://img.shields.io/badge/version-v0.9-blue.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Status](https://img.shields.io/badge/status-active%20development-orange.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Python](https://img.shields.io/badge/python-3.14+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-live-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-supported-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-30%20passing-brightgreen.svg)](https://github.com/Momina29311/ai-resume-screening-system)

ResumeIQ is an AI-powered Resume Screening System that automates the early stages of recruitment by parsing resumes, extracting skills, comparing them against job descriptions, calculating ATS scores, ranking candidates, and providing actionable feedback through an interactive Streamlit dashboard.

This project is being built publicly as part of my Machine Learning and Data Science learning journey.

---

# 🌐 Live Demo

**Streamlit App**

https://momina-resumeiq.streamlit.app

---

# ✨ Features

## 📄 Resume Parsing
- Upload one or multiple PDF resumes
- Extract resume text
- Preview extracted content
- Download extracted text
- Character & word statistics

## 🧠 NLP Preprocessing
- Clean extracted text
- Normalize formatting
- Prepare text for analysis

## 🎯 Skill Extraction
- Detect technical skills
- Skill badge visualization
- Skill comparison against database
- Export extracted skills as JSON

## 🔎 Resume Matching
- Compare resumes with job descriptions
- Detect matched skills
- Detect missing skills
- Calculate match percentage

## ⭐ ATS Score Engine
- Transparent rule-based ATS scoring
- Category-wise score breakdown
- Resume quality feedback
- Personalized recommendations
- JSON score export

### ATS Categories
- Skill Match (40)
- Experience (20)
- Education (15)
- Projects (10)
- Certifications (10)
- Resume Completeness (5)

## 🏆 Candidate Ranking
- Upload multiple resumes
- Compare candidates automatically
- Rank candidates by ATS score
- Identify the best candidate
- Export ranking results

## 🖥 Streamlit Dashboard
- Interactive interface
- Resume upload
- Job description input
- ATS summary cards
- Ranking dashboard
- Feedback & recommendations

## ☁ Deployment
- Streamlit Cloud deployment
- Docker container support
- Portable local development

---

# 📊 Workflow

```text
PDF Resume(s)
      │
      ▼
Resume Parser
      │
      ▼
NLP Preprocessing
      │
      ▼
Skill Extraction
      │
      ▼
Resume-to-Job Matching
      │
      ▼
ATS Score Prediction
      │
      ▼
Candidate Ranking
      │
      ▼
Interactive Dashboard
      │
      ▼
JSON Export
      │
      ▼
Docker & Streamlit Deployment
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

### Version Control
- Git
- GitHub

---

# 📂 Project Structure

```text
ai-resume-screening-system/
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

Current automated test coverage includes:

- Resume Parser
- Resume Matcher
- ATS Score Engine
- Candidate Ranking

**30 Automated Tests Passing**

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

## Build Docker Image

```bash
docker build -t resumeiq .
```

## Run Container

```bash
docker run -p 8501:8501 resumeiq
```

Open:

```
http://localhost:8501
```

---

# 📅 Development Roadmap

| Version | Module | Status |
|----------|--------|--------|
| v0.1 | Project Planning | ✅ |
| v0.2 | Resume Parsing Engine | ✅ |
| v0.3 | NLP Preprocessing | ✅ |
| v0.4 | Skill Extraction | ✅ |
| v0.5 | Resume Matching | ✅ |
| v0.6 | ATS Score Prediction | ✅ |
| v0.7 | Candidate Ranking | ✅ |
| v0.8 | Streamlit Cloud Deployment | ✅ |
| v0.9 | Docker Containerization | ✅ |
| v1.0 | Explainable AI + ML Ranking | 🚧 |

---

# 📈 Future Enhancements

- Explainable AI (XAI)
- Machine Learning–based ATS prediction
- OCR support for scanned resumes
- Semantic skill matching
- Resume database
- Recruiter dashboard
- Authentication
- REST API
- GitHub Actions (CI/CD)
- MLOps pipeline
- Model deployment

---

# 👩‍💻 Author

**Momina Zaheer**

Computer Science Student | AI & Data Science Enthusiast

Building AI projects publicly to learn, improve, and share the journey.

⭐ If you found this project useful, consider giving it a star!