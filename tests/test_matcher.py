from src.matcher import match_resume_to_job


def test_perfect_match():
    resume = ["Python", "SQL", "Docker"]
    job = ["Python", "SQL", "Docker"]
    result = match_resume_to_job(resume, job)
    assert result["match_score"] == 100.0
    assert set(result["matched_skills"]) == {"docker", "python", "sql"}
    assert result["missing_skills"] == []


def test_partial_match():
    resume = ["Python", "SQL"]
    job = ["Python", "SQL", "Docker", "AWS"]
    result = match_resume_to_job(resume, job)
    assert result["match_score"] == 50.0
    assert set(result["matched_skills"]) == {"python", "sql"}
    assert set(result["missing_skills"]) == {"aws", "docker"}


def test_no_match():
    resume = ["Git", "Excel"]
    job = ["Python", "SQL"]
    result = match_resume_to_job(resume, job)
    assert result["match_score"] == 0.0
    assert result["matched_skills"] == []
    assert set(result["missing_skills"]) == {"python", "sql"}


def test_empty_resume():
    resume = []
    job = ["Python", "SQL"]
    result = match_resume_to_job(resume, job)
    assert result["match_score"] == 0.0
    assert result["matched_skills"] == []
    assert set(result["missing_skills"]) == {"python", "sql"}


def test_empty_job_description():
    resume = ["Python", "SQL"]
    job = []
    result = match_resume_to_job(resume, job)
    assert result["match_score"] == 0.0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []


def test_duplicate_skills():
    resume = ["Python", "Python", "SQL", "SQL"]
    job = ["Python", "SQL"]
    result = match_resume_to_job(resume, job)
    assert result["match_score"] == 100.0
    assert set(result["matched_skills"]) == {"python", "sql"}
    assert result["missing_skills"] == []