# 🌲 TrailLens

> **AI that helps you touch grass.**  
> *Identify birds with private, offline AI. Discover one fascinating field mark. Put your phone away and keep exploring.*

[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-Touch%20Grass%20Challenge-emerald.svg)](https://hacktoberfest.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-100%25%20Offline%20PyTorch-blue.svg)](ml/)
[![Model Size](https://img.shields.io/badge/Model%20Size-5.45%20MB-green.svg)](models/)
[![Latency](https://img.shields.io/badge/Inference-22.4%20ms%20(CPU)-orange.svg)](ml/)

---

## 🧭 Product Vision & Core Philosophy

Most outdoor apps are designed like slot machines: they attempt to maximize daily screen time, bombard users with social feeds, and keep their eyes glued to glass.

**TrailLens reverses this paradigm.**

```text
GO OUTSIDE 🌿
     ↓
SEE / HEAR A BIRD 🐦
     ↓
CAPTURE / SELECT PHOTO 📷
     ↓
LOCAL AI IDENTIFICATION (22ms, 0% Cloud) ⚡
     ↓
DISCOVER ONE FASCINATING FIELD MARK 💡
     ↓
EARN XP / STREAKS / BADGES 🎖️
     ↓
PUT PHONE AWAY (Touch Grass Mode) 🔒
     ↓
KEEP EXPLORING THE REAL WORLD 🌳
```

> *"The best TrailLens session is one where the user spends very little time looking at TrailLens."*

---

## 📐 Architecture Diagram

```text
                                TRAILLENS
                                    │
       ┌────────────────────────────┴────────────────────────────┐
       │                                                         │
   Web / Mobile UI (React + Tailwind)                      Local AI Engine
       │                                                         │
       ├── Viewfinder & Photo Ingestion                          ├── Preprocessing & Augmentations
       ├── Audio Synthesizer (Web Audio API)                     ├── MobileNetV3-Small (1.32M Params)
       ├── Touch Grass Exploration HUD                           ├── Uncertainty Calibration & Entropy
       └── Field Guide & Gamification Vault                      └── Rich Species Knowledgebase
       │                                                         │
       └────────────────────────────┬────────────────────────────┘
                                    │
                             Species Result
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                     Confident              Uncertain (<60%)
                         │                     │
                ┌────────┴────────┐     "🤔 I'm not confident yet."
                │                 │     Outdoor observation tips
           Field Guide       Gamification
           (200 Birds)       (XP & Badges)
                │                 │
                └────────┬────────┘
                         │
               [ I'M GOING EXPLORING ]
                         │
                 🌳 TOUCH GRASS 🌳
```

---

## ✨ Key Features

1. **⚡ 100% Offline Local Inference**:
   - Runs fine-tuned PyTorch vision models (MobileNetV3-Small / EfficientNet-B0) on CPU in **<25ms**.
   - Zero cloud API calls, zero cellular dependence, zero latency lag in remote wilderness.
2. **🤔 Calibrated Uncertainty (No Blind Guessing)**:
   - Evaluates softmax confidence and prediction entropy.
   - When an image is blurry or distant, it honestly communicates uncertainty:
     > *"🤔 I'm not confident yet. I think this might be an American Goldfinch (38%). Try: Move closer, improve lighting, ensure the head and beak are in focus."*
3. **🌳 Touch Grass Hero Mode**:
   - Locks distraction elements, displays a tranquil breathing timer, plays subtle ambient nature tones, and tracks outdoor exploration minutes vs. minimal screen time.
4. **🎒 Collectible 200-Species Field Guide**:
   - Complete field guide for North American bird species.
   - Discovered species unlock vibrant full-color cards, audio calls, and rarity stars (1★ to 5★).
   - Undiscovered species appear as mysterious silhouettes with habitat clues.
5. **🔥 Meaningful Outdoor Streaks & Badges**:
   - Streaks are awarded based on **actual outdoor sessions**, not meaningless app opens.
   - 9 collectible achievement badges (First Steps, First Feather, Sharp Eyes, Early Bird, Trail Regular, Night Owl, Bird Nerd, Touch Grass Champion, Master Explorer).
6. **🏆 Activity-Based Leaderboard**:
   - Ranks nature scouts based on verified outdoor exploration minutes and unique species discovered.
7. **🛠️ Developer & Diagnostics HUD**:
   - Real-time diagnostic overlays displaying inference latency, parameter counts, memory usage, and hardware accelerators.

---

## 🔬 ML Pipeline & Model Specifications

| Attribute | Specification |
| :--- | :--- |
| **Model Architecture** | MobileNetV3-Small (fine-grained bird classification head) |
| **Total Parameters** | 1,325,032 (1.32 Million) |
| **Weights Footprint** | 5.45 MB (TorchScript / FP32) |
| **Inference Latency** | 22.4 ms on standard CPU (45+ FPS) |
| **Training Scheme** | Cosine Annealing LR, Label Smoothing (0.1), AdamW, Outdoor Color/Affine Augmentations |
| **Base Weights License** | Apache-2.0 / BSD-3-Clause |
| **Uncertainty Engine** | Softmax Temperature Scaling + Shannon Entropy Thresholding |

### Pluggable Interface
TrailLens provides an abstract `BirdClassifierBase` interface in [`ml/inference.py`](ml/inference.py). Any researcher or developer can swap in alternative backbones (e.g. EfficientNet, ResNet, Swin Transformer) in under 5 lines of code.

---

## 📜 Dataset Provenance & Licenses

TrailLens strictly follows ethical open-source dataset practices. Raw dataset images are **not redistributed or uploaded** to GitHub repositories.

- **CUB-200-2011**: Caltech-UCSD Birds-200-2011 (Wah et al., 2011). 11,788 images across 200 categories. Restricted to non-commercial research and educational purposes.
- **NABirds**: Cornell Lab of Ornithology (Van Horn et al., 2015). 48,562 images across 555 categories. Non-commercial research & educational use.

For complete license terms, citations, and compliance guidelines, see [`DATASET_LICENSES.md`](DATASET_LICENSES.md).

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### 2. Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/traillens.git
cd traillens

# Install Python dependencies
pip install torch torchvision timm scikit-learn pillow fastapi uvicorn psutil python-multipart

# Install Frontend dependencies
cd frontend
npm install
npm run build
cd ..
```

### 3. Launch TrailLens in 1 Click
```bash
python run_app.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

---

## 🧪 Training & Evaluation

### Analyze Local Dataset
```bash
python scripts/analyze_dataset.py
```

### Train Model Checkpoint
```bash
python ml/train.py --arch mobilenet_v3_small --epochs 15 --batch_size 32 --lr 0.001
```

### Run Evaluation & Latency Benchmarks
```bash
python ml/evaluate.py
```

### Export TorchScript Model for Edge
```bash
python ml/export.py
```

### Run Unit Tests
```bash
python -m unittest discover tests -v
```

---

## 🌲 Project Structure

```text
traillens/
├── CUB_200_2011/            # Local dataset directory (not committed)
├── checkpoints/             # Trained model weights (.pth)
├── models/                  # Exported TorchScript model (.pt)
├── data/                    # Species metadata, demo samples, and user states
│   ├── species_metadata.json
│   ├── demo_samples.json
│   └── dataset_summary.json
├── ml/                      # Core Machine Learning package
│   ├── __init__.py
│   ├── dataset.py           # Dataset loader & outdoor augmentations
│   ├── model.py             # Model architecture & parameter counters
│   ├── train.py             # Reproducible training pipeline
│   ├── evaluate.py          # Standalone evaluation & latency benchmarks
│   ├── export.py            # TorchScript export tool
│   └── inference.py         # Local offline inference & uncertainty engine
├── server/                  # Local FastAPI backend
│   └── app.py
├── frontend/                # React + Tailwind + Vite Web Application
│   ├── src/
│   │   ├── components/      # UI screens, Modals, Touch Grass HUD
│   │   ├── utils/           # Web Audio synthesizer & offline API client
│   │   ├── App.jsx
│   │   └── index.css        # Nature-inspired custom design tokens
│   └── index.html
├── scripts/                 # Utility analysis scripts
│   ├── analyze_dataset.py
│   ├── build_species_metadata.py
│   └── prepare_demo_samples.py
├── tests/                   # Complete unittest suite
│   ├── test_dataset.py
│   ├── test_model.py
│   ├── test_inference.py
│   └── test_gamification.py
├── DATASET_LICENSES.md      # Detailed provenance, licenses & citations
├── run_app.py               # 1-Click launcher
└── README.md
```

---

## ⚖️ Open Innovation & Ethical Considerations

1. **Anti-Addiction Design**: No infinite doomscroll feeds. TrailLens congratulates you when your session is over and prompts you to lock your screen.
2. **Wilderness Safety & Privacy**: No GPS coordinates or photo captures are uploaded to cloud servers.
3. **Scientific Integrity**: Species classifications are rooted in verified ornithological databases with clear uncertainty boundaries.

---

## 👥 Credits & Citations

- **CUB-200-2011 Dataset**: California Institute of Technology & UCSD.
- **NABirds Dataset**: Cornell Lab of Ornithology.
- **Torchvision & MobileNet**: PyTorch / Meta AI Research.

---

## 📄 License

This software is licensed under the [MIT License](LICENSE).  
Pretrained model architectures adhere to their respective Apache-2.0 / BSD licenses.  
Dataset images remain the intellectual property of their original photographers under non-commercial educational use terms.
