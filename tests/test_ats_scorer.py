import pytest
from src.ats_score import ATSScorer, ATSScoreBreakdown


@pytest.fixture
def scorer():
    return ATSScorer()


def _make_resume(
    skills=None,
    education=None,
    experience=None,
    projects=None,
    certifications=None,
    sections_present=None,
):
    return {
        "skills": skills or [],
        "education": education or [],
        "experience": experience or [],
        "projects": projects or [],
        "certifications": certifications or [],
        "sections_present": sections_present or {},
    }


def _make_match(match_score=0, skills_found=0, missing_skills=None):
    return {
        "match_score": match_score,
        "skills_found": skills_found,
        "missing_skills": missing_skills or [],
    }


class TestATSScorerEducation:
    def test_no_education(self, scorer):
        resume = _make_resume(education=[])
        result = scorer.score(resume, None)
        assert result.breakdown.education == 0

    def test_unrecognized_degree(self, scorer):
        resume = _make_resume(
            education=[{"degree": "Some Course", "field": "Something"}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.education == 5

    def test_bachelor_degree(self, scorer):
        resume = _make_resume(
            education=[{"degree": "Bachelor", "field": "Computer Science"}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.education == 10

    def test_master_degree(self, scorer):
        resume = _make_resume(
            education=[{"degree": "Master", "field": "Data Science"}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.education == 15

    def test_phd_degree(self, scorer):
        resume = _make_resume(
            education=[{"degree": "PhD", "field": "Machine Learning"}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.education == 15


class TestATSScorerExperience:
    def test_no_experience(self, scorer):
        resume = _make_resume(experience=[])
        result = scorer.score(resume, None)
        assert result.breakdown.experience == 0

    def test_less_than_6_months(self, scorer):
        resume = _make_resume(
            experience=[{"title": "Intern", "duration_months": 4}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.experience == 5

    def test_6_to_12_months(self, scorer):
        resume = _make_resume(
            experience=[{"title": "Intern", "duration_months": 9}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.experience == 10

    def test_1_to_2_years(self, scorer):
        resume = _make_resume(
            experience=[{"title": "Engineer", "duration_months": 18}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.experience == 15

    def test_more_than_2_years(self, scorer):
        resume = _make_resume(
            experience=[{"title": "Engineer", "duration_months": 30}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.experience == 20


class TestATSScorerProjects:
    def test_no_projects(self, scorer):
        resume = _make_resume(projects=[])
        result = scorer.score(resume, None)
        assert result.breakdown.projects == 0

    def test_one_project(self, scorer):
        resume = _make_resume(projects=[{"name": "Project A"}])
        result = scorer.score(resume, None)
        assert result.breakdown.projects == 4

    def test_two_projects(self, scorer):
        resume = _make_resume(
            projects=[{"name": "Project A"}, {"name": "Project B"}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.projects == 7

    def test_three_or_more_projects(self, scorer):
        resume = _make_resume(
            projects=[
                {"name": "Project A"},
                {"name": "Project B"},
                {"name": "Project C"},
            ]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.projects == 10


class TestATSScorerCertifications:
    def test_no_certifications(self, scorer):
        resume = _make_resume(certifications=[])
        result = scorer.score(resume, None)
        assert result.breakdown.certifications == 0

    def test_one_certification(self, scorer):
        resume = _make_resume(
            certifications=[{"name": "AWS Cloud Practitioner"}]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.certifications == 5

    def test_two_or_more_certifications(self, scorer):
        resume = _make_resume(
            certifications=[
                {"name": "AWS Cloud Practitioner"},
                {"name": "TensorFlow Developer"},
            ]
        )
        result = scorer.score(resume, None)
        assert result.breakdown.certifications == 10


class TestATSScorerCompleteness:
    def test_all_sections_present(self, scorer):
        resume = _make_resume(
            sections_present={
                "contact_info": True,
                "summary": True,
                "skills": True,
                "education": True,
                "experience": True,
            }
        )
        result = scorer.score(resume, None)
        assert result.breakdown.completeness == 5

    def test_some_sections_missing(self, scorer):
        resume = _make_resume(
            sections_present={
                "contact_info": True,
                "summary": False,
                "skills": True,
                "education": True,
                "experience": False,
            }
        )
        result = scorer.score(resume, None)
        assert result.breakdown.completeness == 3

    def test_no_sections_present(self, scorer):
        resume = _make_resume(sections_present={})
        result = scorer.score(resume, None)
        assert result.breakdown.completeness == 0


class TestATSScorerSkillMatch:
    def test_zero_match(self, scorer):
        resume = _make_resume()
        match = _make_match(match_score=0)
        result = scorer.score(resume, match)
        assert result.breakdown.skill_match == 0

    def test_50_percent_match(self, scorer):
        resume = _make_resume()
        match = _make_match(match_score=50)
        result = scorer.score(resume, match)
        # 50% of 40 = 20
        assert result.breakdown.skill_match == 20

    def test_100_percent_match(self, scorer):
        resume = _make_resume()
        match = _make_match(match_score=100)
        result = scorer.score(resume, match)
        assert result.breakdown.skill_match == 40


class TestATSScorerFeedback:
    def test_feedback_generated(self, scorer):
        resume = _make_resume(
            education=[{"degree": "Bachelor"}],
            experience=[{"title": "Engineer", "duration_months": 24}],
            projects=[{"name": "P1"}],
            certifications=[{"name": "C1"}],
            sections_present={
                "contact_info": True,
                "summary": True,
                "skills": True,
                "education": True,
                "experience": True,
            },
        )
        match = _make_match(match_score=75, skills_found=10, missing_skills=["docker"])
        result = scorer.score(resume, match)

        assert len(result.feedback) > 0
        assert len(result.recommendations) > 0
        assert any("docker" in r.lower() for r in result.recommendations)


class TestATSScorerOverall:
    def test_excellent_resume(self, scorer):
        resume = _make_resume(
            education=[{"degree": "Master"}],
            experience=[{"title": "Engineer", "duration_months": 36}],
            projects=[{"name": "P1"}, {"name": "P2"}, {"name": "P3"}],
            certifications=[{"name": "C1"}, {"name": "C2"}],
            sections_present={
                "contact_info": True,
                "summary": True,
                "skills": True,
                "education": True,
                "experience": True,
            },
        )
        match = _make_match(match_score=90, skills_found=15, missing_skills=[])
        result = scorer.score(resume, match)

        assert 80 <= result.ats_score <= 100

    def test_average_resume(self, scorer):
        resume = _make_resume(
            education=[{"degree": "Bachelor"}],
            experience=[{"title": "Engineer", "duration_months": 12}],
            projects=[{"name": "P1"}],
            certifications=[{"name": "C1"}],
            sections_present={
                "contact_info": True,
                "summary": True,
                "skills": True,
                "education": True,
                "experience": True,
            },
        )
        match = _make_match(match_score=60, skills_found=8, missing_skills=["aws"])
        result = scorer.score(resume, match)

        assert 50 <= result.ats_score <= 80

    def test_poor_resume(self, scorer):
        resume = _make_resume(
            education=[],
            experience=[],
            projects=[],
            certifications=[],
            sections_present={
                "contact_info": False,
                "summary": False,
                "skills": False,
                "education": False,
                "experience": False,
            },
        )
        match = _make_match(match_score=20, skills_found=2, missing_skills=[])
        result = scorer.score(resume, match)

        assert result.ats_score < 40

    def test_missing_education_only(self, scorer):
        resume = _make_resume(
            education=[],
            experience=[{"title": "Engineer", "duration_months": 24}],
            projects=[{"name": "P1"}, {"name": "P2"}],
            certifications=[{"name": "C1"}],
            sections_present={
                "contact_info": True,
                "summary": True,
                "skills": True,
                "education": False,
                "experience": True,
            },
        )
        match = _make_match(match_score=70, skills_found=9, missing_skills=[])
        result = scorer.score(resume, match)

        assert result.breakdown.education == 0
        assert 50 <= result.ats_score <= 85

    def test_missing_experience_only(self, scorer):
        resume = _make_resume(
            education=[{"degree": "Bachelor"}],
            experience=[],
            projects=[{"name": "P1"}],
            certifications=[],
            sections_present={
                "contact_info": True,
                "summary": True,
                "skills": True,
                "education": True,
                "experience": False,
            },
        )
        match = _make_match(match_score=65, skills_found=7, missing_skills=[])
        result = scorer.score(resume, match)

        assert result.breakdown.experience == 0
        assert 40 <= result.ats_score <= 80

    def test_empty_resume(self, scorer):
        resume = _make_resume()
        match = None
        result = scorer.score(resume, match)

        assert result.ats_score == 0
        assert result.breakdown.skill_match == 0
        assert result.breakdown.education == 0
        assert result.breakdown.experience == 0
        assert result.breakdown.projects == 0
        assert result.breakdown.certifications == 0
        assert result.breakdown.completeness == 0