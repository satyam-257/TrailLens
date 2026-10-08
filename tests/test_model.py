"""
Unit Tests for TrailLens Model Architecture
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import torch
from ml.model import build_model, AVAILABLE_ARCHITECTURES

class TestModel(unittest.TestCase):
    def test_model_instantiation(self):
        for arch in ["mobilenet_v3_small", "resnet18"]:
            model = build_model(architecture=arch, num_classes=200, pretrained=False)
            params = model.count_parameters()
            self.assertTrue(params["total_parameters"] > 0)
            self.assertTrue(params["size_mb_fp32"] < 50, "Lightweight model should be under 50MB")

            dummy_input = torch.randn(2, 3, 224, 224)
            output = model(dummy_input)
            self.assertEqual(output.shape, (2, 200), f"Expected shape (2, 200), got {output.shape}")

if __name__ == "__main__":
    unittest.main()
