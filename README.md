# 🚀 ResumeIQ – AI-Powered Resume Screening System

[![Version](https://img.shields.io/badge/version-v0.6-blue.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Status](https://img.shields.io/badge/status-active%20development-orange.svg)](https://github.com/Momina29311/ai-resume-screening-system)
[![Python](https://img.shields.io/badge/python-3.14+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-app-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/tests-30%20passing-brightgreen.svg)](https://github.com/Momina29311/ai-resume-screening-system)

ResumeIQ is an end-to-end AI-powered resume screening system that parses resumes, preprocesses text with NLP, extracts technical skills, matches resumes to job descriptions, and predicts a transparent ATS score.

This project is being built publicly as part of my machine learning and data science journey.

---

## 📌 Project Overview

ResumeIQ helps automate early-stage resume screening by combining:
- Resume parsing.
- NLP preprocessing.
- Skill extraction.
- Resume-to-job matching.
- ATS score prediction.
- Streamlit-based dashboard visualization.

It is designed to make resume analysis more structured, explainable, and useful for both candidates and recruiters.

---

## ✅ What’s Completed

### Core pipeline
- ✅ Project planning and architecture.
- ✅ Resume parsing engine.
- ✅ NLP preprocessing pipeline.
- ✅ Skill extraction engine.
- ✅ Resume-to-job matching engine.
- ✅ ATS score prediction engine.

### Application layer
- ✅ Streamlit dashboard integration.
- ✅ Resume upload and parsing.
- ✅ Extracted text preview and download.
- ✅ Skill badges and skill comparison table.
- ✅ Match score display.
- ✅ ATS score display with breakdown.
- ✅ Feedback and recommendations section.
- ✅ JSON export for score results.

### Testing
- ✅ Unit tests for ATS scoring.
- ✅ 30 passing ATS tests.

---

## 🆕 Latest Updates

### ResumeIQ v0.6
This version introduced the ATS Score Prediction Engine, which evaluates resume quality beyond simple skill matching.

#### Added in this version
- Weighted ATS scoring system.
- Score breakdown by category.
- Resume quality feedback.
- Personalized suggestions.
- JSON export of ATS results.
- Dashboard metrics for match score, ATS score, skills found, and missing skills.

---

## ⭐ ATS Score Prediction

ResumeIQ now calculates an ATS score using a transparent rule-based system.

### Scoring categories
- Skill Match — 40
- Education — 15
- Experience — 20
- Projects — 10
- Certifications — 10
- Resume Completeness — 5

### Output
The system returns:
- Overall ATS score out of 100.
- Category-wise breakdown.
- Feedback messages.
- Actionable recommendations.
- JSON export for later use.

---

## ✨ Features

### 📄 Resume Parsing
- Upload PDF resumes.
- Extract resume text.
- Preview extracted text.
- Download extracted text.
- View character count and word count.

### 🧠 Skill Extraction
- Detect technical skills from resume text.
- Display detected skills as badges.
- Compare extracted text with the skills database.
- Save detected skills to JSON.

### 🔎 Resume Matching
- Compare resume skills against job description skills.
- Identify matched and missing skills.
- Generate a match score.
- Provide matching recommendations.

### ⭐ ATS Scoring
- Calculate an overall ATS score.
- Use weighted rule-based scoring.
- Break down score by category.
- Generate resume feedback.
- Export ATS results as JSON.

### 🖥 Streamlit Dashboard
- Upload and parse resumes.
- Show metrics and summary cards.
- Display match score and ATS score.
- Show score breakdown, feedback, and recommendations.

---

## 📊 Current Workflow

```text
PDF Resume
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
Dashboard + JSON Export
```

---

## 🖥 Current Interface

- Upload Resume.
- Parse Resume.
- Preview Extracted Text.
- Display Detected Skills.
- Compare Resume with Job Description.
- Show Match Score.
- Show ATS Score.
- Display Score Breakdown.
- Show Feedback and Recommendations.
- Export Results to JSON.

---

## 🛠 Tech Stack

### Programming
- Python

### NLP
- NLTK
- spaCy planned

### PDF Processing
- pdfplumber

### Web Framework
- Streamlit

### Testing
- pytest

---

## 📂 Project Structure

```text
ai-resume-screening-system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── sample_resumes/
│   └── scores/
│
├── src/
│   ├── parser.py
│   ├── preprocessing.py
│   ├── skill_extractor.py
│   ├── matcher.py
│   ├── ats_score.py
│   └── config.py
│
├── models/
├── notebooks/
└── tests/
```

---

## 📂 Testing Summary

| Resume Type | Status |
|--------------|--------|
| Excellent Resume | ✅ |
| Average Resume | ✅ |
| Poor Resume | ✅ |
| Missing Education | ✅ |
| Missing Experience | ✅ |
| Empty Resume | ✅ |

---

## 📅 Development Roadmap

| Version | Module | Status |
|--------|--------|--------|
| v0.1 | Project Planning | ✅ |
| v0.2 | Resume Parsing Engine | ✅ |
| v0.3 | NLP Preprocessing Pipeline | ✅ |
| v0.4 | Skill Extraction Engine | ✅ |
| v0.5 | Resume-to-Job Matching Engine | ✅ |
| v0.6 | ATS Score Prediction Engine | ✅ |
| v0.7 | Candidate Ranking System | ⏳ |
| v0.8 | OCR Support for Scanned Resumes | ⏳ |
| v1.0 | Final Release | 🚀 |

---

## 🚀 Getting Started

### Clone the repository
```bash
git clone https://github.com/Momina29311/ai-resume-screening-system.git
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the app
```bash
streamlit run app.py
```

---

## 📈 Future Enhancements

- OCR support for scanned resumes.
- Candidate ranking system.
- Resume-to-job fit visualization.
- ML-based ATS scoring.
- Docker deployment.
- Cloud deployment.

---

## 👩‍💻 Author

**Momina Zaheer**

Computer Science Student | Aspiring Data Scientist | Aspiring AI & Machine Learning Engineer

Building AI projects publicly to learn, improve, and share the journey.

⭐ If you found this project interesting, consider giving it a star!