"""
Prepare Curated Demo Samples for TrailLens
Extracts high-resolution test photos of iconic birds and creates an uncertainty test case.
"""

import os
import glob
import json
import base64
from PIL import Image
import io

def prepare_samples():
    cub_dir = "CUB_200_2011"
    images_dir = os.path.join(cub_dir, "images")
    metadata_file = os.path.join("data", "species_metadata.json")

    with open(metadata_file, "r", encoding="utf-8") as f:
        all_species = json.load(f)

    species_by_folder = {s["raw_folder"]: s for s in all_species}

    target_folders = [
        ("088.Western_Meadowlark", "Western Meadowlark", "Iconic prairie songbird with bright yellow breast and black V"),
        ("014.Indigo_Bunting", "Indigo Bunting", "Stunning celestial-blue plumage navigating by night stars"),
        ("017.Northern_Cardinal", "Northern Cardinal", "Vibrant crimson crest and sweet territory whistling"),
        ("072.Pomarine_Jaeger", "Pomarine Jaeger", "Oceanic predator known for twisting aerial chases"),
        ("192.Common_Yellowthroat", "Common Yellowthroat", "Curious marsh bird wearing a distinct burglar mask"),
        ("002.Laysan_Albatross", "Laysan Albatross", "Majestic ocean traveler capable of dynamic soaring across open seas"),
        ("196.House_Wren", "House Wren", "Energetic backyard singer with bubbly liquid chatter"),
        ("186.Cedar_Waxwing", "Cedar Waxwing", "Silky crested bird with bright red waxy wing tips"),
    ]

    samples = []
    os.makedirs(os.path.join("data", "demo_images"), exist_ok=True)

    for folder_name, label, desc in target_folders:
        folder_path = os.path.join(images_dir, folder_name)
        if os.path.exists(folder_path):
            img_files = glob.glob(os.path.join(folder_path, "*.jpg"))
            if img_files:
                sample_img_path = img_files[0]
                spec_info = species_by_folder.get(folder_name, {})
                
                # Copy or read image
                with Image.open(sample_img_path) as img:
                    # Save a compressed web-friendly thumbnail
                    img.thumbnail((600, 600))
                    thumb_name = f"{folder_name.split('.')[1].lower()}_thumb.jpg"
                    thumb_path = os.path.join("data", "demo_images", thumb_name)
                    img.save(thumb_path, "JPEG", quality=85)
                    
                    # Also create base64 preview for zero-delay offline loading
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=80)
                    b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

                samples.append({
                    "id": spec_info.get("id", len(samples) + 1),
                    "title": label,
                    "folder": folder_name,
                    "description": desc,
                    "image_path": thumb_path.replace("\\", "/"),
                    "thumbnail_base64": f"data:image/jpeg;base64,{b64_str}",
                    "species_data": spec_info,
                    "test_type": "high_confidence"
                })

    # Add a blurry / ambiguous sample for testing uncertainty communication
    if samples:
        first_img_path = samples[0]["image_path"]
        with Image.open(first_img_path) as img:
            from PIL import ImageFilter
            blurred = img.filter(ImageFilter.GaussianBlur(radius=15))
            blur_name = "ambiguous_uncertainty_sample.jpg"
            blur_path = os.path.join("data", "demo_images", blur_name)
            blurred.save(blur_path, "JPEG", quality=70)

            buffered = io.BytesIO()
            blurred.save(buffered, format="JPEG", quality=70)
            b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            samples.append({
                "id": 999,
                "title": "Distant / Blurry Silhouette (Uncertainty Test)",
                "folder": "uncertainty_test",
                "description": "Demonstrates honest AI calibration when confidence is low",
                "image_path": blur_path.replace("\\", "/"),
                "thumbnail_base64": f"data:image/jpeg;base64,{b64_str}",
                "species_data": {
                    "common_name": "Unidentified Aves",
                    "scientific_name": "Incerta avis",
                    "family": "Unknown",
                    "rarity": 1,
                    "base_xp": 25,
                    "fact": "Always look closely at posture and wing silhouettes when lighting is low!"
                },
                "test_type": "uncertainty_demo"
            })

    out_file = os.path.join("data", "demo_samples.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)

    print(f"[OK] Generated {len(samples)} curated demo samples at {out_file}")

if __name__ == "__main__":
    prepare_samples()
