from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ATSScoreBreakdown:
    skill_match: int = 0
    education: int = 0
    experience: int = 0
    projects: int = 0
    certifications: int = 0
    completeness: int = 0

    def total(self) -> int:
        return (
            self.skill_match
            + self.education
            + self.experience
            + self.projects
            + self.certifications
            + self.completeness
        )


@dataclass
class ATSResult:
    ats_score: int
    breakdown: ATSScoreBreakdown
    feedback: List[str] = field(default_factory=list)
    match_score: int = 0
    skills_found: int = 0
    missing_skills: int = 0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ats_score": self.ats_score,
            "match_score": self.match_score,
            "skills_found": self.skills_found,
            "missing_skills": self.missing_skills,
            "breakdown": {
                "skill_match": self.breakdown.skill_match,
                "education": self.breakdown.education,
                "experience": self.breakdown.experience,
                "projects": self.breakdown.projects,
                "certifications": self.breakdown.certifications,
                "completeness": self.breakdown.completeness,
            },
            "feedback": self.feedback,
            "recommendations": self.recommendations,
        }


class ATSScorer:
    def score(
        self,
        parsed_resume: Dict[str, Any],
        match_result: Dict[str, Any] | None = None,
    ) -> ATSResult:
        match_score = 0
        if match_result:
            match_score = min(100, max(0, match_result.get("match_score", 0)))

        skill_match_score = int(round((match_score / 100.0) * 40))
        education_score = self._score_education(parsed_resume.get("education", []))
        experience_score = self._score_experience(parsed_resume.get("experience", []))
        projects_score = self._score_projects(parsed_resume.get("projects", []))
        certifications_score = self._score_certifications(parsed_resume.get("certifications", []))
        completeness_score = self._score_completeness(parsed_resume)

        breakdown = ATSScoreBreakdown(
            skill_match=skill_match_score,
            education=education_score,
            experience=experience_score,
            projects=projects_score,
            certifications=certifications_score,
            completeness=completeness_score,
        )

        feedback, recommendations = self._generate_feedback(
            parsed_resume,
            match_result,
            breakdown,
        )

        return ATSResult(
            ats_score=breakdown.total(),
            breakdown=breakdown,
            feedback=feedback,
            match_score=match_score,
            skills_found=match_result.get("skills_found", 0) if match_result else 0,
            missing_skills=match_result.get("missing_skills", 0) if match_result else 0,
            recommendations=recommendations,
        )

    def _score_education(self, education_list: List[Dict[str, Any]]) -> int:
        if not education_list:
            return 0

        max_level = 0
        for edu in education_list:
            degree = (edu.get("degree") or "").lower()
            if "phd" in degree or "doctor" in degree:
                max_level = max(max_level, 3)
            elif "master" in degree or "ms" in degree or "m.tech" in degree:
                max_level = max(max_level, 3)
            elif "bachelor" in degree or "bs" in degree or "b.tech" in degree or "be" in degree:
                max_level = max(max_level, 2)
            else:
                max_level = max(max_level, 1)

        if max_level == 1:
            return 5
        if max_level == 2:
            return 10
        return 15

    def _score_experience(self, experience_list: List[Dict[str, Any]]) -> int:
        if not experience_list:
            return 0

        total_months = 0
        for exp in experience_list:
            months = exp.get("duration_months", 0) or 0
            total_months += max(0, int(months))

        if total_months < 6:
            return 5
        if total_months < 12:
            return 10
        if total_months < 24:
            return 15
        return 20

    def _score_projects(self, projects_list: List[Dict[str, Any]]) -> int:
        count = len(projects_list) if projects_list else 0
        if count == 0:
            return 0
        if count == 1:
            return 4
        if count == 2:
            return 7
        return 10

    def _score_certifications(self, certs_list: List[Dict[str, Any]]) -> int:
        count = len(certs_list) if certs_list else 0
        if count == 0:
            return 0
        if count == 1:
            return 5
        return 10

    def _score_completeness(self, parsed_resume: Dict[str, Any]) -> int:
        sections = parsed_resume.get("sections_present", {})
        required_sections = ["contact_info", "summary", "skills", "education", "experience"]
        present_count = sum(1 for sec in required_sections if sections.get(sec, False))
        return min(5, present_count)

    def _generate_feedback(
        self,
        parsed_resume: Dict[str, Any],
        match_result: Dict[str, Any] | None,
        breakdown: ATSScoreBreakdown,
    ) -> tuple[List[str], List[str]]:
        feedback = []
        recommendations = []

        if breakdown.skill_match >= 32:
            feedback.append("✅ Strong technical skills alignment with the job.")
        elif breakdown.skill_match >= 20:
            feedback.append("⚠ Moderate skill match; consider adding missing key skills.")
        else:
            feedback.append("❌ Low skill match; review required skills for the role.")

        if breakdown.education >= 10:
            feedback.append("✅ Education section detected with recognized degree.")
        elif breakdown.education > 0:
            feedback.append("⚠ Education section present but could be clearer.")
            recommendations.append("Clearly mention your degree name and field.")
        else:
            feedback.append("❌ No education information detected.")
            recommendations.append("Add an Education section with degree and institution.")

        if breakdown.experience >= 15:
            feedback.append("✅ Solid work experience.")
        elif breakdown.experience > 0:
            feedback.append("⚠ Limited experience detected.")
            recommendations.append("Add more details about roles, responsibilities, and duration.")
        else:
            feedback.append("❌ No experience section detected.")
            recommendations.append("Include internships, jobs, or relevant projects as experience.")

        if breakdown.projects >= 7:
            feedback.append("✅ Good number of projects.")
        elif breakdown.projects > 0:
            feedback.append("⚠ A few projects detected; consider adding more.")
            recommendations.append("Add 2–3 substantial projects with tech stack and outcomes.")
        else:
            feedback.append("❌ No projects section detected.")
            recommendations.append("Add a Projects section with clear descriptions and results.")

        if breakdown.certifications >= 10:
            feedback.append("✅ Multiple certifications present.")
        elif breakdown.certifications > 0:
            feedback.append("⚠ Some certifications present.")
            recommendations.append("Add any additional relevant certifications (e.g., cloud, ML).")
        else:
            feedback.append("❌ No certifications detected.")
            recommendations.append("Consider adding relevant certifications to strengthen your profile.")

        if breakdown.completeness >= 4:
            feedback.append("✅ Resume appears largely complete.")
        else:
            feedback.append("⚠ Resume may be missing important sections.")
            recommendations.append("Ensure you have Contact, Summary, Skills, Education, and Experience sections.")

        if match_result:
            missing = match_result.get("missing_skills", [])
            if missing:
                recommendations.append(f"Add or highlight these missing skills: {', '.join(missing[:5])}.")

        return feedback, recommendations[:5]