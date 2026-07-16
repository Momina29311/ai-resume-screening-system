# 🚀 ResumeIQ – AI-Powered Resume Screening System

An end-to-end AI-powered Resume Screening System that parses resumes, preprocesses text using NLP, extracts technical skills, and intelligently matches resumes with job descriptions.

> 🚧 Currently under active development as part of my #100DaysOfMachineLearning journey.

---

## 📌 Project Status

**Current Version:** `v0.3`

### Completed Modules

- ✅ Project Initialization
- ✅ Resume Parsing Engine
- ✅ NLP Preprocessing Pipeline

### Upcoming Modules

- ⬜ Skill Extraction Engine
- ⬜ Resume Matching
- ⬜ ATS Scoring
- ⬜ Streamlit Dashboard Improvements
- ⬜ Model Deployment

---

# 🏗 Project Structure

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
│   └── sample_resumes/
│
├── src/
│   ├── parser.py
│   ├── preprocessing.py
│   ├── utils.py
│   └── config.py
│
├── models/
│
├── notebooks/
│
└── tests/
```

---

# ✨ Features

### 📄 Resume Parsing

- Upload PDF resumes
- Extract resume text
- Preview extracted text
- Download extracted text
- Character count
- Word count

---

### 🧠 NLP Preprocessing

- Text Cleaning
- Lowercasing
- Whitespace Normalization
- Text Formatting
- Ready for Skill Extraction

---

# 📊 Current Workflow

```text
PDF Resume
      │
      ▼
Resume Parser
      │
      ▼
Raw Resume Text
      │
      ▼
NLP Preprocessing
      │
      ▼
Clean Resume Text
      │
      ▼
(Skill Extraction - Coming Soon)
```

---

# 🖥 Current Interface

✔ Upload Resume

✔ Parse Resume

✔ Preview Text

✔ Character Statistics

✔ Word Statistics

✔ Download Processed Text

---

# 🛠 Tech Stack

### Programming

- Python

### NLP

- NLTK
- spaCy (planned)

### PDF Processing

- pdfplumber

### Web Framework

- Streamlit

### Testing

- pytest

---

# 📂 Testing Summary

The parser has been evaluated on multiple resume layouts.

| Resume Type | Status |
|--------------|--------|
| ATS Resume | ✅ |
| Modern Resume | ✅ |
| Two Column Resume | ⚠️ |
| Scanned Resume | ❌ |
| Sample Resume | ✅ |

---

# 📅 Development Roadmap

| Version | Module | Status |
|-----------|--------|--------|
| v0.1 | Project Planning | ✅ |
| v0.2 | Resume Parsing Engine | ✅ |
| v0.3 | NLP Preprocessing Pipeline | ✅ |
| v0.4 | Skill Extraction | 🔄 |
| v0.5 | Resume Matching | ⏳ |
| v0.6 | ATS Scoring | ⏳ |
| v0.7 | Dashboard Improvements | ⏳ |
| v1.0 | Final Release | 🚀 |

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/Momina29311/ai-resume-screening-system.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

---

# 📷 Screenshots

## Resume Upload

> *(Add a screenshot of your application here.)*

## Resume Preview

> *(Add another screenshot after parsing.)*

---

# 📈 Future Enhancements

- OCR Support
- Skill Extraction
- Resume Ranking
- ATS Compatibility Score
- Job Description Matching
- Resume Recommendation
- Docker Deployment
- Cloud Deployment

---

# 👩‍💻 Author

**Momina Zaheer**

Computer Science Student | Aspiring AI & Machine Learning Engineer

Building AI projects publicly to learn, improve, and share the journey.

⭐ If you found this project interesting, consider giving it a star!