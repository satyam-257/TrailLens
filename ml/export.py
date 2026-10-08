"""
TrailLens Model Exporter
Exports PyTorch weights to optimized TorchScript (.pt) and ONNX formats
for cross-platform, local edge deployment without Python ML runtime overhead.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
from ml.model import build_model

def export_model(
    checkpoint_path="checkpoints/mobilenet_v3_small_best.pth",
    architecture="mobilenet_v3_small",
    output_dir="models",
    input_size=(1, 3, 224, 224)
):
    os.makedirs(output_dir, exist_ok=True)
    device = torch.device("cpu") # Export for CPU execution

    model = build_model(architecture=architecture, num_classes=200, pretrained=False)
    if os.path.exists(checkpoint_path):
        ckpt = torch.load(checkpoint_path, map_location=device)
        model.load_state_dict(ckpt["state_dict"])
        print(f"[*] Loaded checkpoint from {checkpoint_path}")
    else:
        print(f"[*] Initializing model with default weights for export")

    model.eval()
    dummy_input = torch.randn(*input_size)

    # 1. Export TorchScript
    ts_path = os.path.join(output_dir, "traillens_model.pt")
    traced_model = torch.jit.trace(model, dummy_input)
    traced_model.save(ts_path)
    ts_size_mb = round(os.path.getsize(ts_path) / (1024 * 1024), 2)
    print(f"[OK] Exported TorchScript Model -> {ts_path} ({ts_size_mb} MB)")

    # 2. Export ONNX if supported
    onnx_path = os.path.join(output_dir, "traillens_model.onnx")
    try:
        torch.onnx.export(
            model,
            dummy_input,
            onnx_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=["input"],
            output_names=["logits"],
            dynamic_axes={"input": {0: "batch_size"}, "logits": {0: "batch_size"}}
        )
        onnx_size_mb = round(os.path.getsize(onnx_path) / (1024 * 1024), 2)
        print(f"[OK] Exported ONNX Model -> {onnx_path} ({onnx_size_mb} MB)")
    except Exception as e:
        print(f"[!] ONNX export skipped: {e}")

    return {
        "torchscript_path": ts_path,
        "torchscript_size_mb": ts_size_mb
    }

if __name__ == "__main__":
    export_model()
