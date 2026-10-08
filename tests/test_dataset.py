"""
Unit Tests for TrailLens Dataset Pipeline
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import torch
from ml.dataset import CUB200Dataset, get_transforms

class TestDataset(unittest.TestCase):
    def test_cub_dataset_loading(self):
        if not os.path.exists("CUB_200_2011"):
            self.skipTest("CUB_200_2011 directory not found.")

        ds = CUB200Dataset(base_dir="CUB_200_2011", split="train")
        self.assertTrue(len(ds) > 0, "Train dataset should contain samples")
        
        img, label, iid = ds[0]
        self.assertIsInstance(img, torch.Tensor, "Image should be converted to Tensor")
        self.assertEqual(img.shape, (3, 224, 224), f"Image shape should be (3, 224, 224), got {img.shape}")
        self.assertTrue(0 <= label < 200, f"Label {label} should be in [0, 199]")

    def test_transforms(self):
        tr_train = get_transforms(img_size=224, split="train")
        tr_val = get_transforms(img_size=224, split="val")
        self.assertIsNotNone(tr_train)
        self.assertIsNotNone(tr_val)

if __name__ == "__main__":
    unittest.main()
