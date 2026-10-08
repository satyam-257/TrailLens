"""
TrailLens Training Pipeline
End-to-end reproducible training script with Top-1/Top-5 accuracy, Cosine Annealing,
Label Smoothing, validation tracking, checkpoint export, and evaluation metrics logging.
"""

import os
import sys

# Ensure root directory in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import json
import argparse
import random
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ml.dataset import CUB200Dataset, get_transforms
from ml.model import build_model

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def compute_accuracy(output, target, topk=(1, 5)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size).item())
        return res

def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    running_top1 = 0.0
    running_top5 = 0.0
    total_samples = 0

    for images, targets, _ in loader:
        images = images.to(device)
        targets = targets.to(device)
        batch_size = images.size(0)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        top1, top5 = compute_accuracy(outputs, targets, topk=(1, 5))
        running_loss += loss.item() * batch_size
        running_top1 += top1 * batch_size
        running_top5 += top5 * batch_size
        total_samples += batch_size

    return (
        running_loss / total_samples,
        running_top1 / total_samples,
        running_top5 / total_samples
    )

def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_top1 = 0.0
    running_top5 = 0.0
    total_samples = 0

    with torch.no_grad():
        for images, targets, _ in loader:
            images = images.to(device)
            targets = targets.to(device)
            batch_size = images.size(0)

            outputs = model(images)
            loss = criterion(outputs, targets)

            top1, top5 = compute_accuracy(outputs, targets, topk=(1, 5))
            running_loss += loss.item() * batch_size
            running_top1 += top1 * batch_size
            running_top5 += top5 * batch_size
            total_samples += batch_size

    return (
        running_loss / total_samples,
        running_top1 / total_samples,
        running_top5 / total_samples
    )

def run_training(
    dataset_dir="CUB_200_2011",
    architecture="mobilenet_v3_small",
    epochs=5,
    batch_size=32,
    lr=0.001,
    weight_decay=1e-4,
    output_dir="checkpoints",
    seed=42,
    max_train_samples=None
):
    set_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Starting TrailLens Training")
    print(f"    Architecture: {architecture}")
    print(f"    Device: {device}")
    print(f"    Dataset Dir: {dataset_dir}")
    print(f"    Epochs: {epochs} | Batch Size: {batch_size} | LR: {lr}")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Datasets
    train_dataset = CUB200Dataset(base_dir=dataset_dir, split="train", seed=seed)
    val_dataset = CUB200Dataset(base_dir=dataset_dir, split="val", seed=seed)
    test_dataset = CUB200Dataset(base_dir=dataset_dir, split="test", seed=seed)

    if max_train_samples and max_train_samples < len(train_dataset.sample_ids):
        train_dataset.sample_ids = train_dataset.sample_ids[:max_train_samples]

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"    Train Samples: {len(train_dataset)} | Val: {len(val_dataset)} | Test: {len(test_dataset)}")

    # Model
    model = build_model(architecture=architecture, num_classes=200, pretrained=True)
    model = model.to(device)
    param_info = model.count_parameters()
    print(f"    Model Parameters: {param_info['total_parameters']:,} (~{param_info['size_mb_fp32']} MB)")

    # Loss & Optimizer
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    best_val_top1 = 0.0
    history = []

    start_time = time.time()
    for epoch in range(1, epochs + 1):
        ep_start = time.time()
        tr_loss, tr_top1, tr_top5 = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_top1, val_top5 = evaluate(model, val_loader, criterion, device)
        scheduler.step()
        ep_dur = time.time() - ep_start

        print(f"Epoch [{epoch:02d}/{epochs:02d}] ({ep_dur:.1f}s) | "
              f"Train Loss: {tr_loss:.4f} Acc@1: {tr_top1:.2f}% Acc@5: {tr_top5:.2f}% | "
              f"Val Loss: {val_loss:.4f} Acc@1: {val_top1:.2f}% Acc@5: {val_top5:.2f}%")

        epoch_stats = {
            "epoch": epoch,
            "train_loss": round(tr_loss, 4),
            "train_top1": round(tr_top1, 2),
            "train_top5": round(tr_top5, 2),
            "val_loss": round(val_loss, 4),
            "val_top1": round(val_top1, 2),
            "val_top5": round(val_top5, 2),
            "lr": optimizer.param_groups[0]["lr"],
            "duration_sec": round(ep_dur, 2)
        }
        history.append(epoch_stats)

        # Save best model
        if val_top1 >= best_val_top1:
            best_val_top1 = val_top1
            best_path = os.path.join(output_dir, f"{architecture}_best.pth")
            torch.save({
                "epoch": epoch,
                "architecture": architecture,
                "num_classes": 200,
                "state_dict": model.state_dict(),
                "val_top1": val_top1,
                "val_top5": val_top5,
                "param_info": param_info
            }, best_path)
            print(f"    [--> Saved Best Checkpoint ({val_top1:.2f}% Top-1) to {best_path}]")

    # Evaluate on final test set
    test_loss, test_top1, test_top5 = evaluate(model, test_loader, criterion, device)
    total_time = time.time() - start_time
    print(f"\n[OK] Training Finished in {total_time/60:.2f} minutes")
    print(f"     Final Test Acc@1: {test_top1:.2f}% | Acc@5: {test_top5:.2f}%")

    metrics_file = os.path.join("data", "training_metrics.json")
    summary = {
        "architecture": architecture,
        "epochs": epochs,
        "batch_size": batch_size,
        "device": str(device),
        "total_training_time_sec": round(total_time, 2),
        "param_info": param_info,
        "best_val_top1": best_val_top1,
        "test_results": {
            "loss": round(test_loss, 4),
            "top1_accuracy": round(test_top1, 2),
            "top5_accuracy": round(test_top5, 2)
        },
        "history": history
    }
    with open(metrics_file, "w") as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", type=str, default="mobilenet_v3_small")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--samples", type=int, default=None)
    args = parser.parse_args()

    run_training(
        architecture=args.arch,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        max_train_samples=args.samples
    )
