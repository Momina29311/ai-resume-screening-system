import os
import json
import pytest

from src.ranking import rank_candidates, save_ranking_results


@pytest.fixture
def skills_db():
    return ["python", "sql", "machine learning", "data analysis", "excel"]


@pytest.fixture
def job_description():
    return "We need Python, SQL, and Machine Learning experience."


@pytest.fixture
def parsed_resumes():
    return [
        {
            "name": "Alex.pdf",
            "text": "Python SQL Machine Learning Data Analysis",
            "skills": ["python", "sql", "machine learning", "data analysis"],
        },
        {
            "name": "Maya.pdf",
            "text": "Python SQL Excel",
            "skills": ["python", "sql", "excel"],
        },
        {
            "name": "Jordan.pdf",
            "text": "Python only",
            "skills": ["python"],
        },
    ]


def test_ranking_order(parsed_resumes, job_description, skills_db):
    ranked = rank_candidates(parsed_resumes, job_description, skills_db)
    assert ranked[0]["name"] == "Alex.pdf"


def test_highest_score_first(parsed_resumes, job_description, skills_db):
    ranked = rank_candidates(parsed_resumes, job_description, skills_db)
    scores = [item["ats_score"] for item in ranked]
    assert scores == sorted(scores, reverse=True)


def test_empty_resume_list(job_description, skills_db):
    ranked = rank_candidates([], job_description, skills_db)
    assert ranked == []


def test_duplicate_scores(job_description, skills_db):
    resumes = [
        {"name": "A.pdf", "text": "Python SQL", "skills": ["python", "sql"]},
        {"name": "B.pdf", "text": "Python SQL", "skills": ["python", "sql"]},
    ]
    ranked = rank_candidates(resumes, job_description, skills_db)
    assert len(ranked) == 2
    assert ranked[0]["ats_score"] == ranked[1]["ats_score"]


def test_sorting_correctness(job_description, skills_db):
    resumes = [
        {"name": "Low.pdf", "text": "Python", "skills": ["python"]},
        {"name": "High.pdf", "text": "Python SQL Machine Learning", "skills": ["python", "sql", "machine learning"]},
    ]
    ranked = rank_candidates(resumes, job_description, skills_db)
    assert ranked[0]["name"] == "High.pdf"


def test_save_ranking_results(tmp_path):
    data = [{"name": "Alex", "ats_score": 91}]
    output_file = tmp_path / "ranking_results.json"
    path = save_ranking_results(data, str(output_file))
    assert os.path.exists(path)

    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded[0]["name"] == "Alex"