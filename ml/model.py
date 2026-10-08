"""
TrailLens Model Architecture & Abstraction
Provides pluggable model backends for lightweight, open-weight vision architectures
specifically optimized for low-latency offline inference on CPU and mobile devices.
"""

import torch
import torch.nn as nn
from torchvision import models
from typing import Dict, Any, Tuple

AVAILABLE_ARCHITECTURES = [
    "mobilenet_v3_small",
    "mobilenet_v3_large",
    "efficientnet_b0",
    "resnet18"
]

class TrailLensClassifier(nn.Module):
    """
    Fine-grained bird classification model with customizable backbone
    and regularized classification head with dropout and label-smoothing readiness.
    """
    def __init__(
        self,
        architecture: str = "mobilenet_v3_small",
        num_classes: int = 200,
        pretrained: bool = True,
        dropout: float = 0.2
    ):
        super().__init__()
        self.architecture = architecture
        self.num_classes = num_classes
        
        if architecture == "mobilenet_v3_small":
            weights = models.MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
            backbone = models.mobilenet_v3_small(weights=weights)
            in_features = backbone.classifier[0].in_features
            # Replace classifier
            backbone.classifier = nn.Sequential(
                nn.Linear(in_features, 512),
                nn.Hardswish(),
                nn.Dropout(p=dropout),
                nn.Linear(512, num_classes)
            )
            self.model = backbone

        elif architecture == "mobilenet_v3_large":
            weights = models.MobileNet_V3_Large_Weights.DEFAULT if pretrained else None
            backbone = models.mobilenet_v3_large(weights=weights)
            in_features = backbone.classifier[0].in_features
            backbone.classifier = nn.Sequential(
                nn.Linear(in_features, 1024),
                nn.Hardswish(),
                nn.Dropout(p=dropout),
                nn.Linear(1024, num_classes)
            )
            self.model = backbone

        elif architecture == "efficientnet_b0":
            weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
            backbone = models.efficientnet_b0(weights=weights)
            in_features = backbone.classifier[1].in_features
            backbone.classifier = nn.Sequential(
                nn.Dropout(p=dropout),
                nn.Linear(in_features, num_classes)
            )
            self.model = backbone

        elif architecture == "resnet18":
            weights = models.ResNet18_Weights.DEFAULT if pretrained else None
            backbone = models.resnet18(weights=weights)
            in_features = backbone.fc.in_features
            backbone.fc = nn.Sequential(
                nn.Dropout(p=dropout),
                nn.Linear(in_features, num_classes)
            )
            self.model = backbone

        else:
            raise ValueError(f"Unsupported architecture: {architecture}. Supported: {AVAILABLE_ARCHITECTURES}")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def count_parameters(self) -> Dict[str, int]:
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return {
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "size_mb_fp32": round((total_params * 4) / (1024 * 1024), 2),
            "size_mb_int8": round((total_params * 1) / (1024 * 1024), 2)
        }

def build_model(
    architecture: str = "mobilenet_v3_small",
    num_classes: int = 200,
    pretrained: bool = True,
    dropout: float = 0.2
) -> TrailLensClassifier:
    """Factory helper to instantiate a TrailLens classifier"""
    return TrailLensClassifier(
        architecture=architecture,
        num_classes=num_classes,
        pretrained=pretrained,
        dropout=dropout
    )
