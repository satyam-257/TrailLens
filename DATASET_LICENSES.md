# Dataset Provenance, Licenses & Usage Policies

TrailLens strictly adheres to open-source ethical data practices and dataset licensing terms. This document details the provenance, license constraints, usage permissions, and citation requirements for all datasets integrated and supported by TrailLens.

---

## 1. CUB-200-2011 (Caltech-UCSD Birds-200-2011)

### Overview
- **Dataset Name**: Caltech-UCSD Birds-200-2011 (CUB-200-2011)
- **Creators / Maintainers**: California Institute of Technology & University of California, San Diego (Wah et al., 2011)
- **Official URL**: [http://www.vision.caltech.edu/visipedia/CUB-200-2011.html](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html)
- **Total Images**: 11,788
- **Total Categories**: 200 North American bird species
- **Splits**: 5,994 Training / 5,794 Testing

### License & Permitted Use
- **License Type**: **Non-commercial Research & Educational Use Only**.
- **Commercial Restrictions**: Images within CUB-200-2011 are collected from Flickr and other public web platforms. The dataset creators specify that the images are made available strictly for non-commercial academic research and educational evaluation.
- **Redistribution Policy**:
  - TrailLens **does NOT redistribute, package, or host** CUB-200-2011 image files in any public repository or web bundle.
  - Image paths in TrailLens are fully decoupled and configurable via local environment configurations.
  - Users and developers must acquire the dataset directly from authorized academic mirrors according to Caltech-UCSD instructions.

### Citation
```bibtex
@techreport{WahCUB_200_2011,
    Title = {{The Caltech-UCSD Birds-200-2011 Dataset}},
    Author = {Wah, C. and Branson, S. and Welinder, P. and Perona, P. and Belongie, S.},
    Year = {2011},
    Institution = {California Institute of Technology},
    Number = {CNS-TR-2011-001}
}
```

---

## 2. NABirds (North American Birds Dataset)

### Overview
- **Dataset Name**: NABirds V1
- **Creators / Maintainers**: Cornell Lab of Ornithology & Visipedia Research Group (Van Horn et al., 2015)
- **Official URL**: [https://dl.allaboutbirds.org/nabirds](https://dl.allaboutbirds.org/nabirds)
- **Total Images**: 48,562 annotated photographs
- **Total Categories**: 555 visual categories (404 species)

### License & Permitted Use
- **License Type**: **Non-commercial Research & Educational Use Only**.
- **Commercial Restrictions**: Images are provided courtesy of photographers from the Cornell Lab of Ornithology and Macaulay Library for research and educational purposes.
- **Redistribution Policy**:
  - Image archives are NOT distributed with the source code.
  - Automated downloader scripts point directly to verified institutional endpoints.

### Citation
```bibtex
@inproceedings{vanhorn2015building,
    title={Building a Bird Recognition App and Large Scale Dataset with Citizen Scientists: The Fine Print in Fine-Grained Dataset Collection},
    author={Van Horn, Grant and Branson, Steve and Farrell, Ryan and Haber, Scott and Barry, Jessie and Ipeirotis, Panos and Perona, Pietro and Belongie, Serge},
    booktitle={CVPR},
    year={2015}
}
```

---

## 3. Pretrained Model Weights & Open-Source AI Licenses

| Component | Architecture | Base Weights License | Origin / Source |
| :--- | :--- | :--- | :--- |
| **MobileNetV3-Small** | PyTorch / Torchvision | Apache 2.0 / BSD 3-Clause | PyTorch Official Models (`torchvision.models`) |
| **MobileNetV3-Large** | PyTorch / Torchvision | Apache 2.0 / BSD 3-Clause | PyTorch Official Models (`torchvision.models`) |
| **EfficientNet-B0** | PyTorch / Timm | Apache 2.0 | Ross Wightman / PyTorch Image Models (`timm`) |

### Model Portability & Local Offline Guarantee
- All model weights are open-weight architectures runnable on CPU and Edge hardware without cloud calls.
- Developers can fine-tune or replace models seamlessly using the abstract `BirdClassifierBase` interface.
- No proprietary cloud APIs (e.g. OpenAI, Google Cloud Vision, Azure Cognitive Services) are utilized for real-time inference.

---

## 4. Summary of Compliance Principles

1. **No Data Laundering**: All training pipelines explicitly document source annotations.
2. **Zero Unauthorized Redistribution**: Raw image archives remain on user machines and are ignored via `.gitignore`.
3. **Transparent Uncertainty**: The classification engine explicitly indicates uncertainty and refusal boundaries rather than hallucinating species.
4. **Offline-First by Design**: Everything runs on `localhost` without transmitting user photos to external servers, protecting outdoor privacy.
