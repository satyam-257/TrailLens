"""
TrailLens Local Bird Identification & Uncertainty Engine
Executes ultra-fast offline inference on local CPU/GPU, communicates calibration & uncertainty,
and enriches predictions with field guide facts and outdoor missions.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import io
import time
import json
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from PIL import Image

import torch
import torch.nn.functional as F
from torchvision import transforms

from ml.model import build_model

class BirdIdentifierBase(ABC):
    """
    Abstract interface for Bird Identification models in TrailLens.
    Enables zero-friction plug-and-play model replacement.
    """
    @abstractmethod
    def identify(self, image_input: Union[str, bytes, Image.Image], top_k: int = 5) -> Dict[str, Any]:
        """Runs identification on an image and returns structured prediction results with confidence"""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Returns model metadata, parameter counts, and license information"""
        pass

class LocalVisionIdentifier(BirdIdentifierBase):
    """
    Production-grade local vision identifier using PyTorch/TorchScript.
    100% offline, private, and deterministic with uncertainty thresholds.
    """
    def __init__(
        self,
        model_path: Optional[str] = None,
        metadata_path: str = "data/species_metadata.json",
        architecture: str = "mobilenet_v3_small",
        confidence_threshold: float = 0.60,
        uncertainty_entropy_threshold: float = 2.5,
        temperature: float = 1.0,
        device: Optional[str] = None
    ):
        self.architecture = architecture
        self.confidence_threshold = confidence_threshold
        self.uncertainty_entropy_threshold = uncertainty_entropy_threshold
        self.temperature = temperature
        
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        # Load Species Metadata
        self.species_metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                for item in raw_list:
                    self.species_metadata[item["class_index"]] = item
        else:
            print(f"[Warning] Species metadata {metadata_path} not found.")

        # Load Model
        self.model = build_model(architecture=architecture, num_classes=200, pretrained=True)
        self.model_loaded_from = "pretrained_base"

        if model_path and os.path.exists(model_path):
            try:
                ckpt = torch.load(model_path, map_location=self.device)
                if isinstance(ckpt, dict) and "state_dict" in ckpt:
                    self.model.load_state_dict(ckpt["state_dict"])
                else:
                    self.model.load_state_dict(ckpt)
                self.model_loaded_from = model_path
                print(f"[OK] Loaded fine-tuned checkpoint: {model_path}")
            except Exception as e:
                print(f"[!] Checkpoint load failed ({e}), using default weights.")

        self.model = self.model.to(self.device)
        self.model.eval()

        # Image Transform
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def _preprocess(self, image_input: Union[str, bytes, Image.Image]) -> torch.Tensor:
        if isinstance(image_input, str):
            image = Image.open(image_input).convert("RGB")
        elif isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, Image.Image):
            image = image_input.convert("RGB")
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")

        tensor = self.transform(image).unsqueeze(0)
        return tensor.to(self.device)

    def identify(self, image_input: Union[str, bytes, Image.Image], top_k: int = 5) -> Dict[str, Any]:
        t0 = time.perf_counter()
        
        # Preprocess
        tensor = self._preprocess(image_input)
        prep_time_ms = round((time.perf_counter() - t0) * 1000, 2)

        # Inference
        t1 = time.perf_counter()
        with torch.no_grad():
            logits = self.model(tensor)
            scaled_logits = logits / self.temperature
            probabilities = F.softmax(scaled_logits, dim=-1)[0]
        
        infer_time_ms = round((time.perf_counter() - t1) * 1000, 2)
        total_latency_ms = round((time.perf_counter() - t0) * 1000, 2)

        # Calculate prediction entropy for uncertainty estimation
        probs_np = probabilities.cpu().numpy()
        entropy = -np.sum(probs_np * np.log(probs_np + 1e-12))

        # Top K predictions
        top_probs, top_indices = torch.topk(probabilities, k=min(top_k, len(probabilities)))
        top_probs = top_probs.cpu().tolist()
        top_indices = top_indices.cpu().tolist()

        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            meta = self.species_metadata.get(idx, {
                "id": idx + 1,
                "common_name": f"Species #{idx + 1}",
                "scientific_name": "Aves indet.",
                "family": "Unknown",
                "habitat": "Outdoors",
                "rarity": 2,
                "base_xp": 75,
                "conservation_status": "Least Concern",
                "fact": "Fascinating bird seen in the wild!",
                "audio_cue": "Sweet chirping call.",
                "outdoor_mission": "Spot another in the wild!"
            })
            predictions.append({
                "class_index": idx,
                "confidence_score": round(prob, 4),
                "confidence_percentage": round(prob * 100, 1),
                "species": meta
            })

        top_pred = predictions[0]
        confidence = top_pred["confidence_score"]

        # Uncertainty evaluation
        is_confident = confidence >= self.confidence_threshold and entropy < self.uncertainty_entropy_threshold
        
        uncertainty_notice = None
        if not is_confident:
            if confidence < 0.40:
                uncertainty_notice = {
                    "level": "low",
                    "headline": "I'm not confident yet.",
                    "message": f"I think this might be {top_pred['species']['common_name']} ({top_pred['confidence_percentage']}%), but the signal is fuzzy.",
                    "tips": [
                        "Move closer or zoom in gently without disturbing the bird",
                        "Ensure the head and beak are in clear focus",
                        "Wait for better sunlight or adjust angle to reduce backlighting"
                    ]
                }
            else:
                uncertainty_notice = {
                    "level": "moderate",
                    "headline": "Likely match, but double check field marks!",
                    "message": f"Looks like {top_pred['species']['common_name']} ({top_pred['confidence_percentage']}%). Compare the field marks below.",
                    "tips": [
                        "Verify plumage coloration on the wings and chest",
                        "Listen for the species call",
                        "Check if the habitat matches"
                    ]
                }

        # Playful microcopy
        microcopy_options = [
            "Nice spotting! 👀",
            "Field guide match verified. 🌿",
            "Sharp eyes out on the trail! 🔭",
            "Added to your nature discovery log. 🎒"
        ]
        microcopy = microcopy_options[int(top_indices[0]) % len(microcopy_options)]

        return {
            "success": True,
            "is_confident": is_confident,
            "uncertainty_notice": uncertainty_notice,
            "top_prediction": top_pred,
            "all_predictions": predictions,
            "uncertainty_metrics": {
                "entropy": round(float(entropy), 3),
                "confidence_threshold": self.confidence_threshold
            },
            "performance": {
                "preprocessing_ms": prep_time_ms,
                "inference_ms": infer_time_ms,
                "total_latency_ms": total_latency_ms,
                "device": str(self.device),
                "offline_local": True
            },
            "microcopy": microcopy
        }

    def get_model_info(self) -> Dict[str, Any]:
        param_counts = self.model.count_parameters()
        return {
            "model_name": f"TrailLens-{self.architecture.replace('_', '-').title()}",
            "architecture": self.architecture,
            "license": "Apache-2.0 / BSD-3-Clause",
            "source": "PyTorch / Torchvision Open-Weight Models",
            "parameters": param_counts["total_parameters"],
            "size_mb": param_counts["size_mb_fp32"],
            "device": str(self.device),
            "offline_ready": True,
            "num_classes": 200,
            "input_resolution": "224x224 RGB",
            "description": "Lightweight open-weight vision backbone fine-tuned for on-device bird identification."
        }
