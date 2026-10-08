"""
Dataset Analysis and Verification Tool for TrailLens
Analyzes CUB-200-2011 (and NABirds if available), extracts distributions, image dimensions,
class balance, bounding boxes, and generates statistical summaries.
"""

import os
import json
import numpy as np
from PIL import Image
from collections import Counter
import time

def analyze_cub_dataset(base_dir="CUB_200_2011"):
    print(f"[*] Analyzing CUB-200-2011 dataset at: {base_dir}")
    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Directory {base_dir} not found.")

    classes_file = os.path.join(base_dir, "classes.txt")
    images_file = os.path.join(base_dir, "images.txt")
    split_file = os.path.join(base_dir, "train_test_split.txt")
    labels_file = os.path.join(base_dir, "image_class_labels.txt")
    bbox_file = os.path.join(base_dir, "bounding_boxes.txt")
    images_dir = os.path.join(base_dir, "images")

    # Load classes
    classes = {}
    with open(classes_file, "r") as f:
        for line in f:
            if line.strip():
                cid, cname = line.strip().split(" ", 1)
                clean_name = " ".join(cname.split(".")[1].split("_"))
                classes[int(cid)] = {
                    "raw_name": cname,
                    "clean_name": clean_name
                }

    # Load images
    images = {}
    with open(images_file, "r") as f:
        for line in f:
            if line.strip():
                iid, iname = line.strip().split(" ", 1)
                images[int(iid)] = iname

    # Load splits
    splits = {}
    with open(split_file, "r") as f:
        for line in f:
            if line.strip():
                iid, is_train = line.strip().split()
                splits[int(iid)] = int(is_train)

    # Load labels
    labels = {}
    with open(labels_file, "r") as f:
        for line in f:
            if line.strip():
                iid, cid = line.strip().split()
                labels[int(iid)] = int(cid)

    # Load bboxes
    bboxes = {}
    if os.path.exists(bbox_file):
        with open(bbox_file, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split()
                    iid = int(parts[0])
                    x, y, w, h = map(float, parts[1:])
                    bboxes[iid] = [x, y, w, h]

    # Compute class distributions
    class_counts = Counter(labels.values())
    train_class_counts = Counter([labels[iid] for iid, is_tr in splits.items() if is_tr == 1])
    test_class_counts = Counter([labels[iid] for iid, is_tr in splits.items() if is_tr == 0])

    print(f"Total images: {len(images)}")
    print(f"Total classes: {len(classes)}")
    print(f"Train images: {sum(splits.values())} ({sum(splits.values())/len(images)*100:.1f}%)")
    print(f"Test images: {len(images) - sum(splits.values())} ({(len(images) - sum(splits.values()))/len(images)*100:.1f}%)")

    # Sample image dimension check (sampling 500 images for speed)
    widths, heights, aspect_ratios, formats = [], [], [], []
    sample_ids = list(images.keys())[::max(1, len(images)//500)]
    
    for iid in sample_ids:
        rel_path = images[iid]
        full_path = os.path.join(images_dir, rel_path)
        if os.path.exists(full_path):
            try:
                with Image.open(full_path) as img:
                    w, h = img.size
                    widths.append(w)
                    heights.append(h)
                    aspect_ratios.append(round(w / h, 2))
                    formats.append(img.format)
            except Exception as e:
                pass

    summary = {
        "dataset_name": "CUB-200-2011 (Caltech-UCSD Birds-200-2011)",
        "num_images": len(images),
        "num_classes": len(classes),
        "train_images": sum(splits.values()),
        "test_images": len(images) - sum(splits.values()),
        "class_balance": {
            "min_per_class": min(class_counts.values()),
            "max_per_class": max(class_counts.values()),
            "mean_per_class": float(np.mean(list(class_counts.values()))),
            "std_per_class": float(np.std(list(class_counts.values())))
        },
        "sample_dimensions": {
            "samples_checked": len(widths),
            "mean_width": float(np.mean(widths)) if widths else 0,
            "mean_height": float(np.mean(heights)) if heights else 0,
            "min_width": int(np.min(widths)) if widths else 0,
            "max_width": int(np.max(widths)) if widths else 0,
            "min_height": int(np.min(heights)) if heights else 0,
            "max_height": int(np.max(heights)) if heights else 0,
            "formats": dict(Counter(formats))
        },
        "annotations_present": {
            "bounding_boxes": len(bboxes) == len(images),
            "part_locations": os.path.exists(os.path.join(base_dir, "parts", "part_locs.txt")),
            "attributes": os.path.exists(os.path.join(base_dir, "attributes", "image_attribute_labels.txt")),
            "train_test_split": True
        },
        "sample_classes": [
            {"id": cid, "name": cinfo["clean_name"], "raw": cinfo["raw_name"], "count": class_counts[cid]}
            for cid, cinfo in list(classes.items())[:10]
        ]
    }

    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "dataset_summary.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[OK] Dataset analysis complete! Summary saved to {out_path}")
    return summary

if __name__ == "__main__":
    analyze_cub_dataset()
