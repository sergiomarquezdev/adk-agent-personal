"""
Unit tests for CV data extractor functions.
"""

import unittest
from unittest.mock import patch

from personal_agent.tools.cv.extractors import (
    get_certificates,
    get_education,
    get_personal_info,
    get_projects,
    get_skills,
    get_work_experience,
)

# A sample CV data structure to be returned by the mocked get_cv_data
SAMPLE_CV_DATA = {
    "basics": {
        "name": "Sergio Márquez",
        "label": "AI/ML Developer",
        "email": "contact@sergiomarquez.dev",
        "summary": "A summary.",
        "location": {"city": "Málaga"},
        "profiles": [{"network": "LinkedIn", "url": "a-url"}],
    },
    "work": [{"name": "PwC", "position": "AI/ML Developer"}],
    "education": [{"institution": "Universidad de Málaga", "area": "Ingeniería de Software"}],
    "certificates": [{"name": "Machine Learning Specialization", "issuer": "Coursera"}],
    "skills": {
        "highlighted": ["Python", "FastAPI"],
        "other": ["JavaScript"],
        "databases": ["PostgreSQL"],
    },
    "projects": [{"name": "Agente Personal con ADK"}],
}


class TestCVExtractors(unittest.TestCase):
    """
    Test suite for functions in extractors.py.
    It patches get_cv_data to return a consistent sample CV,
    isolating the extractor functions from the cache/download logic.
    """

    @patch("personal_agent.tools.cv.extractors.get_cv_data")
    def test_get_personal_info(self, mock_get_cv_data):
        mock_get_cv_data.return_value = SAMPLE_CV_DATA
        info = get_personal_info()
        self.assertEqual(info["name"], "Sergio Márquez")
        self.assertEqual(info["label"], "AI/ML Developer")
        self.assertIn("profiles", info)

    @patch("personal_agent.tools.cv.extractors.get_cv_data")
    def test_get_work_experience(self, mock_get_cv_data):
        mock_get_cv_data.return_value = SAMPLE_CV_DATA
        experience = get_work_experience()
        self.assertIsInstance(experience, list)
        self.assertEqual(len(experience), 1)
        self.assertEqual(experience[0]["name"], "PwC")

    @patch("personal_agent.tools.cv.extractors.get_cv_data")
    def test_get_education(self, mock_get_cv_data):
        mock_get_cv_data.return_value = SAMPLE_CV_DATA
        education = get_education()
        self.assertIsInstance(education, list)
        self.assertEqual(len(education), 1)
        self.assertEqual(education[0]["institution"], "Universidad de Málaga")

    @patch("personal_agent.tools.cv.extractors.get_cv_data")
    def test_get_skills(self, mock_get_cv_data):
        mock_get_cv_data.return_value = SAMPLE_CV_DATA
        skills = get_skills()
        self.assertIn("highlighted", skills)
        self.assertIn("Python", skills["highlighted"])
        self.assertIn("other", skills)
        self.assertIn("databases", skills)

    @patch("personal_agent.tools.cv.extractors.get_cv_data")
    def test_get_projects(self, mock_get_cv_data):
        mock_get_cv_data.return_value = SAMPLE_CV_DATA
        projects = get_projects()
        self.assertIsInstance(projects, list)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["name"], "Agente Personal con ADK")

    @patch("personal_agent.tools.cv.extractors.get_cv_data")
    def test_get_certificates(self, mock_get_cv_data):
        mock_get_cv_data.return_value = SAMPLE_CV_DATA
        certificates = get_certificates()
        self.assertIsInstance(certificates, list)
        self.assertEqual(len(certificates), 1)
        self.assertEqual(certificates[0]["issuer"], "Coursera")

    @patch("personal_agent.tools.cv.extractors.get_cv_data")
    def test_empty_cv_data(self, mock_get_cv_data):
        """Test that functions handle empty or missing CV data gracefully."""
        mock_get_cv_data.return_value = None
        self.assertEqual(get_personal_info(), {"error": "No se pudo obtener el CV"})
        self.assertEqual(get_work_experience(), [{"error": "No se pudo obtener el CV"}])
        self.assertEqual(get_education(), [{"error": "No se pudo obtener el CV"}])
        self.assertEqual(get_skills(), {"error": "No se pudo obtener el CV"})
        self.assertEqual(get_projects(), [{"error": "No se pudo obtener el CV"}])
        self.assertEqual(get_certificates(), [{"error": "No se pudo obtener el CV"}])


if __name__ == "__main__":
    unittest.main()
