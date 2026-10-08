"""
Unit Tests for TrailLens Inference & Uncertainty Engine
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from PIL import Image
import numpy as np
from ml.inference import LocalVisionIdentifier

class TestInference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.identifier = LocalVisionIdentifier(architecture="mobilenet_v3_small")

    def test_inference_runs_offline(self):
        img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        result = self.identifier.identify(pil_img, top_k=5)
        self.assertTrue(result["success"])
        self.assertIn("top_prediction", result)
        self.assertIn("all_predictions", result)
        self.assertEqual(len(result["all_predictions"]), 5)
        self.assertTrue(result["performance"]["offline_local"])
        self.assertTrue(result["performance"]["total_latency_ms"] > 0)

    def test_uncertainty_handling(self):
        uncertain_identifier = LocalVisionIdentifier(architecture="mobilenet_v3_small", confidence_threshold=0.99)
        noise_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
        result = uncertain_identifier.identify(noise_img)
        
        self.assertFalse(result["is_confident"])
        self.assertIsNotNone(result["uncertainty_notice"])
        self.assertIn("tips", result["uncertainty_notice"])

if __name__ == "__main__":
    unittest.main()
