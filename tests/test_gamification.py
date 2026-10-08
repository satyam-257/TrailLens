"""
Unit Tests for TrailLens Gamification Logic and Server Endpoints
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from fastapi.testclient import TestClient
from server.app import app, get_title_for_level

class TestGamificationAndServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_level_titles(self):
        self.assertEqual(get_title_for_level(1), "Curious Human")
        self.assertEqual(get_title_for_level(5), "Trail Scout")
        self.assertEqual(get_title_for_level(12), "Field Observer")
        self.assertEqual(get_title_for_level(25), "Nature Nerd")
        self.assertEqual(get_title_for_level(35), "Bird Whisperer")
        self.assertEqual(get_title_for_level(55), "Forest Legend")

    def test_health_endpoint(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["offline_mode"])

    def test_species_catalog_endpoint(self):
        res = self.client.get("/api/species")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["total_species"], 200)
        self.assertEqual(len(data["results"]), 200)

    def test_demo_samples_endpoint(self):
        res = self.client.get("/api/demo-samples")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("samples", data)
        self.assertTrue(len(data["samples"]) > 0)

    def test_user_profile_and_session_recording(self):
        res = self.client.get("/api/user/profile")
        self.assertEqual(res.status_code, 200)
        init_xp = res.json()["total_xp"]

        sess_res = self.client.post("/api/user/session", json={
            "duration_minutes": 25,
            "app_seconds": 30,
            "discoveries_count": 1
        })
        self.assertEqual(sess_res.status_code, 200)
        sess_data = sess_res.json()
        self.assertTrue(sess_data["success"])
        self.assertGreater(sess_data["total_xp"], init_xp)

if __name__ == "__main__":
    unittest.main()
