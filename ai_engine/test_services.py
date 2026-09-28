from unittest.mock import patch

from django.test import SimpleTestCase

from .services import _experience_years, _keyword_similarity, _matched_skills, _normalize_skill_name


class ParsingServiceTests(SimpleTestCase):
    def test_experience_years_returns_highest_value(self):
        text = "Software Engineer with 2 years experience and 3.5 years in backend development."
        self.assertEqual(_experience_years(text), 3.5)

    def test_skill_aliases_are_normalized(self):
        self.assertEqual(_normalize_skill_name("ReactJS"), "React")
        self.assertEqual(_normalize_skill_name("Postgres"), "PostgreSQL")

    @patch("ai_engine.services._canonical_skills", return_value=("React", "PostgreSQL", "Python"))
    def test_matched_skills_support_aliases(self, _canonical_skills):
        matches = _matched_skills("ReactJS, PostgreSQL and Python")
        self.assertEqual(matches, ["PostgreSQL", "Python", "React"])

    def test_keyword_similarity_is_bounded(self):
        score = _keyword_similarity("Python Django PostgreSQL", "Python Django REST APIs")
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
