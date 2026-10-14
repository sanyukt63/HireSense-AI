from django.test import SimpleTestCase

from .services import _education_mentions


class EducationMentionTests(SimpleTestCase):
    def test_detects_common_degrees(self):
        self.assertEqual(
            _education_mentions("B.Tech graduate with a Master's degree"),
            ["master", "b.tech"],
        )

    def test_does_not_match_degree_text_inside_larger_words(self):
        self.assertEqual(_education_mentions("masterful communication and bachelorhood"), [])

    def test_is_case_insensitive(self):
        self.assertIn("phd", _education_mentions("PHD in Computer Science"))
