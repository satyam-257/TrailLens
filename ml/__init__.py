"""
TrailLens Machine Learning Package
"""

from ml.dataset import CUB200Dataset, get_transforms
from ml.model import TrailLensClassifier, build_model, AVAILABLE_ARCHITECTURES
from ml.inference import BirdIdentifierBase, LocalVisionIdentifier

__all__ = [
    "CUB200Dataset",
    "get_transforms",
    "TrailLensClassifier",
    "build_model",
    "AVAILABLE_ARCHITECTURES",
    "BirdIdentifierBase",
    "LocalVisionIdentifier"
]
