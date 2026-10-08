"""
TrailLens Dataset Pipeline
Handles CUB-200-2011, NABirds, and generic outdoor bird datasets with
robust outdoor augmentations, train/val/test splits, and bounding box support.
"""

import os
import torch
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms

class CUB200Dataset(Dataset):
    """
    CUB-200-2011 Dataset loader with official train/test splits,
    optional bounding box cropping, and outdoor-specific augmentations.
    """
    def __init__(
        self,
        base_dir="CUB_200_2011",
        split="train",  # 'train', 'test', 'val'
        transform=None,
        use_bbox=False,
        val_ratio=0.1,
        seed=42
    ):
        self.base_dir = base_dir
        self.split = split
        self.use_bbox = use_bbox
        
        images_file = os.path.join(base_dir, "images.txt")
        split_file = os.path.join(base_dir, "train_test_split.txt")
        labels_file = os.path.join(base_dir, "image_class_labels.txt")
        bbox_file = os.path.join(base_dir, "bounding_boxes.txt")
        self.images_dir = os.path.join(base_dir, "images")

        if not os.path.exists(images_file):
            raise FileNotFoundError(f"CUB dataset not found in {base_dir}")

        # Load images
        self.image_paths = {}
        with open(images_file, "r") as f:
            for line in f:
                if line.strip():
                    iid, iname = line.strip().split(" ", 1)
                    self.image_paths[int(iid)] = iname

        # Load labels (1-indexed -> 0-indexed)
        self.labels = {}
        with open(labels_file, "r") as f:
            for line in f:
                if line.strip():
                    iid, cid = line.strip().split()
                    self.labels[int(iid)] = int(cid) - 1

        # Load splits
        self.splits = {}
        with open(split_file, "r") as f:
            for line in f:
                if line.strip():
                    iid, is_tr = line.strip().split()
                    self.splits[int(iid)] = int(is_tr)

        # Load bboxes
        self.bboxes = {}
        if os.path.exists(bbox_file):
            with open(bbox_file, "r") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split()
                        iid = int(parts[0])
                        x, y, w, h = map(float, parts[1:])
                        self.bboxes[iid] = [x, y, w, h]

        # Filter by split
        all_train_ids = [iid for iid, is_tr in self.splits.items() if is_tr == 1]
        test_ids = [iid for iid, is_tr in self.splits.items() if is_tr == 0]

        if split in ["train", "val"]:
            # Deterministic train/val split
            torch.manual_seed(seed)
            perm = torch.randperm(len(all_train_ids)).tolist()
            val_count = int(len(all_train_ids) * val_ratio)
            
            if split == "train":
                selected_indices = perm[val_count:]
                self.sample_ids = [all_train_ids[i] for i in selected_indices]
            else: # val
                selected_indices = perm[:val_count]
                self.sample_ids = [all_train_ids[i] for i in selected_indices]
        else: # test
            self.sample_ids = test_ids

        # Set default transformations if not provided
        if transform is not None:
            self.transform = transform
        else:
            self.transform = get_transforms(split=split)

    def __len__(self):
        return len(self.sample_ids)

    def __getitem__(self, idx):
        iid = self.sample_ids[idx]
        rel_path = self.image_paths[iid]
        full_path = os.path.join(self.images_dir, rel_path)
        
        image = Image.open(full_path).convert("RGB")
        
        if self.use_bbox and iid in self.bboxes:
            x, y, w, h = self.bboxes[iid]
            # Ensure valid bounds
            img_w, img_h = image.size
            x1 = max(0, int(x))
            y1 = max(0, int(y))
            x2 = min(img_w, int(x + w))
            y2 = min(img_h, int(y + h))
            if x2 > x1 and y2 > y1:
                image = image.crop((x1, y1, x2, y2))

        if self.transform:
            image = self.transform(image)

        label = self.labels[iid]
        return image, label, iid

def get_transforms(img_size=224, split="train"):
    """
    Standard and augmented outdoor vision transformations.
    Includes color jitter and slight affine shifts to simulate variable outdoor lighting.
    """
    # ImageNet stats
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )

    if split == "train":
        return transforms.Compose([
            transforms.RandomResizedCrop(img_size, scale=(0.7, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15),
            transforms.RandomRotation(degrees=10),
            transforms.ToTensor(),
            normalize
        ])
    else:
        return transforms.Compose([
            transforms.Resize(int(img_size * 1.14)),
            transforms.CenterCrop(img_size),
            transforms.ToTensor(),
            normalize
        ])
