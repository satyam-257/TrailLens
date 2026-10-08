"""
TrailLens Model Evaluation & Latency Benchmarking
Computes Top-1, Top-5, per-class metrics, confusion matrices, and latency measurements.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

from ml.dataset import CUB200Dataset
from ml.model import build_model

def benchmark_latency(model, device, num_runs=50, input_size=(1, 3, 224, 224)):
    model.eval()
    dummy_input = torch.randn(*input_size).to(device)
    
    # Warmup
    for _ in range(10):
        with torch.no_grad():
            _ = model(dummy_input)

    latencies = []
    for _ in range(num_runs):
        t0 = time.perf_counter()
        with torch.no_grad():
            _ = model(dummy_input)
        latencies.append((time.perf_counter() - t0) * 1000) # ms

    return {
        "mean_latency_ms": round(float(np.mean(latencies)), 2),
        "median_latency_ms": round(float(np.median(latencies)), 2),
        "p95_latency_ms": round(float(np.percentile(latencies, 95)), 2),
        "fps": round(1000.0 / float(np.mean(latencies)), 1)
    }

def evaluate_model(
    checkpoint_path="checkpoints/mobilenet_v3_small_best.pth",
    dataset_dir="CUB_200_2011",
    batch_size=32,
    architecture="mobilenet_v3_small",
    max_test_samples=None
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Evaluating TrailLens Model on {device}")
    
    # Load model
    model = build_model(architecture=architecture, num_classes=200, pretrained=False)
    if os.path.exists(checkpoint_path):
        ckpt = torch.load(checkpoint_path, map_location=device)
        model.load_state_dict(ckpt["state_dict"])
        print(f"    Loaded weights from {checkpoint_path}")
    else:
        print(f"    [Warning] Checkpoint {checkpoint_path} not found. Evaluating base weights.")

    model = model.to(device)
    model.eval()

    # Benchmark latency
    bench_results = benchmark_latency(model, device)
    print(f"    Inference Latency: {bench_results['mean_latency_ms']} ms ({bench_results['fps']} FPS)")

    test_dataset = CUB200Dataset(base_dir=dataset_dir, split="test")
    if max_test_samples and max_test_samples < len(test_dataset.sample_ids):
        test_dataset.sample_ids = test_dataset.sample_ids[:max_test_samples]

    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    all_preds = []
    all_targets = []
    top5_correct = 0
    total_samples = 0

    with torch.no_grad():
        for images, targets, _ in test_loader:
            images = images.to(device)
            targets = targets.to(device)
            outputs = model(images)

            probs = torch.softmax(outputs, dim=-1)
            _, top5 = probs.topk(5, dim=-1)
            
            top1_preds = top5[:, 0]
            all_preds.extend(top1_preds.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())

            for i in range(targets.size(0)):
                if targets[i] in top5[i]:
                    top5_correct += 1
            total_samples += targets.size(0)

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)

    top1_acc = np.mean(all_preds == all_targets) * 100.0
    top5_acc = (top5_correct / total_samples) * 100.0

    precision, recall, f1, _ = precision_recall_fscore_support(
        all_targets, all_preds, average="macro", zero_division=0
    )

    results = {
        "architecture": architecture,
        "total_test_samples": total_samples,
        "top1_accuracy": round(top1_acc, 2),
        "top5_accuracy": round(top5_acc, 2),
        "macro_precision": round(float(precision), 4),
        "macro_recall": round(float(recall), 4),
        "macro_f1": round(float(f1), 4),
        "latency_benchmark": bench_results,
        "model_parameters": model.count_parameters()
    }

    os.makedirs("data", exist_ok=True)
    out_file = os.path.join("data", "evaluation_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[OK] Evaluation Summary:")
    print(f"     Top-1 Accuracy: {results['top1_accuracy']}%")
    print(f"     Top-5 Accuracy: {results['top5_accuracy']}%")
    print(f"     Macro F1 Score: {results['macro_f1']}")
    print(f"     Mean Latency:   {bench_results['mean_latency_ms']} ms/image")
    print(f"     Results written to {out_file}")

    return results

if __name__ == "__main__":
    evaluate_model()
