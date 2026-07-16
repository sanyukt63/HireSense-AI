from django.test import SimpleTestCase

from .services import build_resume_suggestions


class ResumeSuggestionTests(SimpleTestCase):
    def test_build_resume_suggestions_returns_actionable_recommendations(self):
        extracted_data = {
            "skills": ["Python", "Django"],
            "experience_years": 2,
            "education": ["bachelor"],
            "projects": [],
            "certifications": [],
        }

        suggestions = build_resume_suggestions(extracted_data)

        self.assertIn("missing_skills", suggestions)
        self.assertIn("better_keywords", suggestions)
        self.assertIn("formatting_tips", suggestions)
        self.assertIn("suggested_certifications", suggestions)
        self.assertIn("suggested_projects", suggestions)
        self.assertTrue(suggestions["missing_skills"])
