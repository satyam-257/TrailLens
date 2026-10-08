"""
TrailLens 1-Click Unified Runner
Starts the local FastAPI backend and serves the interactive frontend at http://localhost:8000
"""

import os
import sys
import uvicorn
import webbrowser

if __name__ == "__main__":
    port = 8000
    host = "127.0.0.1"
    url = f"http://{host}:{port}"
    print("=" * 60)
    print("[*] Starting TrailLens -- AI Outdoor Bird Identifier")
    print("    Hacktoberfest: Touch Grass Edition")
    print(f"    Local Server: {url}")
    print("    AI Engine:    100% Offline PyTorch MobileNetV3")
    print("=" * 60)
    
    # Run uvicorn server
    uvicorn.run("server.app:app", host=host, port=port, reload=False)
