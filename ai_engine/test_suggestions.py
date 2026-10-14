from django.test import SimpleTestCase

from .services import build_resume_suggestions


class ResumeSuggestionTests(SimpleTestCase):
    def test_suggestions_report_skills_missing_from_resume(self):
        result = build_resume_suggestions({"skills": ["Python", "SQL"]})
        self.assertNotIn("Python", result["missing_skills"])
        self.assertNotIn("SQL", result["missing_skills"])
        self.assertIn("Django", result["missing_skills"])

    def test_empty_resume_returns_actionable_defaults(self):
        result = build_resume_suggestions({})
        self.assertTrue(result["formatting_tips"])
        self.assertTrue(result["suggested_projects"])
        self.assertIn("Machine Learning", result["better_keywords"])
