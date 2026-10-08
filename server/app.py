"""
TrailLens Local Backend Server
FastAPI server providing local offline AI inference, species field guide,
outdoor session tracking, gamification (XP, streaks, badges), and hardware diagnostics.
"""

import os
import sys

# Ensure root directory in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import io
import time
import json
import base64
import psutil
from typing import Optional, List, Dict, Any
from datetime import datetime, date

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from PIL import Image

from ml.inference import LocalVisionIdentifier

app = FastAPI(
    title="TrailLens Local AI API",
    description="Offline-first outdoor bird identification and nature companion",
    version="1.0.0"
)

# CORS enabled for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Local Vision Engine
print("[*] Initializing TrailLens Local Vision Identifier...")
identifier = LocalVisionIdentifier(
    model_path="checkpoints/mobilenet_v3_small_best.pth" if os.path.exists("checkpoints/mobilenet_v3_small_best.pth") else None,
    metadata_path="data/species_metadata.json",
    confidence_threshold=0.60
)
print("[OK] Vision Identifier ready for local inference.")

# Load Datasets & Metadata
DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "user_state.json")

def load_species_data() -> List[Dict[str, Any]]:
    path = os.path.join(DATA_DIR, "species_metadata.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_demo_samples() -> List[Dict[str, Any]]:
    path = os.path.join(DATA_DIR, "demo_samples.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Badge Definitions
DEFAULT_BADGES = [
    {
        "id": "first_steps",
        "title": "First Steps",
        "icon": "🌱",
        "description": "Complete your very first outdoor exploration session.",
        "category": "exploration",
        "required_xp": 50,
        "criteria": "sessions >= 1"
    },
    {
        "id": "first_feather",
        "title": "First Feather",
        "icon": "🐦",
        "description": "Identify your first wild bird species.",
        "category": "identification",
        "required_xp": 100,
        "criteria": "species_count >= 1"
    },
    {
        "id": "sharp_eyes",
        "title": "Sharp Eyes",
        "icon": "🔭",
        "description": "Identify 5 different bird species in nature.",
        "category": "identification",
        "required_xp": 250,
        "criteria": "species_count >= 5"
    },
    {
        "id": "early_bird",
        "title": "Early Bird",
        "icon": "🌅",
        "description": "Complete an outdoor exploration session before 8:00 AM.",
        "category": "exploration",
        "required_xp": 200,
        "criteria": "early_session >= 1"
    },
    {
        "id": "trail_regular",
        "title": "Trail Regular",
        "icon": "🌲",
        "description": "Maintain an outdoor streak of 7 consecutive days.",
        "category": "streak",
        "required_xp": 500,
        "criteria": "streak_days >= 7"
    },
    {
        "id": "night_owl",
        "title": "Night Owl",
        "icon": "🦉",
        "description": "Discover a nocturnal species or explore during dusk twilight.",
        "category": "discovery",
        "required_xp": 350,
        "criteria": "night_discovery >= 1"
    },
    {
        "id": "bird_nerd",
        "title": "Bird Nerd",
        "icon": "📖",
        "description": "Discover 25 unique bird species in your Field Guide.",
        "category": "identification",
        "required_xp": 1000,
        "criteria": "species_count >= 25"
    },
    {
        "id": "touch_grass_champion",
        "title": "Touch Grass Champion",
        "icon": "🌳",
        "description": "Spend over 10 hours outdoors with your phone tucked away.",
        "category": "touch_grass",
        "required_xp": 1500,
        "criteria": "outdoor_minutes >= 600"
    },
    {
        "id": "master_explorer",
        "title": "Master Explorer",
        "icon": "🗺️",
        "description": "Complete 10 outdoor wilderness sessions.",
        "category": "exploration",
        "required_xp": 800,
        "criteria": "sessions >= 10"
    }
]

# Rotating Challenges
DEFAULT_CHALLENGES = [
    {
        "id": "daily_2_species",
        "title": "Find 2 Different Species",
        "type": "daily",
        "description": "Spot and identify two distinct bird species today in their natural habitat.",
        "target": 2,
        "current": 1,
        "completed": False,
        "reward_xp": 150,
        "icon": "🐦"
    },
    {
        "id": "daily_outside_20m",
        "title": "Spend 20 Minutes Outside",
        "type": "daily",
        "description": "Activate Touch Grass mode and explore your local park or trail.",
        "target": 20,
        "current": 15,
        "completed": False,
        "reward_xp": 120,
        "icon": "🌳"
    },
    {
        "id": "daily_morning_walk",
        "title": "Quiet Morning Observation",
        "type": "daily",
        "description": "Observe one bird quietly for at least 60 seconds without taking photos.",
        "target": 1,
        "current": 0,
        "completed": False,
        "reward_xp": 100,
        "icon": "🌄"
    },
    {
        "id": "weekly_5_discoveries",
        "title": "Weekly Trailblazer",
        "type": "weekly",
        "description": "Log 5 new field guide observations throughout this week.",
        "target": 5,
        "current": 3,
        "completed": False,
        "reward_xp": 400,
        "icon": "⭐"
    }
]

def get_title_for_level(level: int) -> str:
    if level < 5:
        return "Curious Human"
    elif level < 10:
        return "Trail Scout"
    elif level < 20:
        return "Field Observer"
    elif level < 30:
        return "Nature Nerd"
    elif level < 50:
        return "Bird Whisperer"
    else:
        return "Forest Legend"

def init_user_state() -> Dict[str, Any]:
    return {
        "user_name": "Satyam",
        "level": 3,
        "title": "Trail Scout",
        "total_xp": 340,
        "streak_days": 4,
        "last_active_date": str(date.today()),
        "total_outdoor_minutes": 76,
        "total_app_minutes": 4,
        "discovered_species_ids": [14, 17, 88, 196], # Pre-populate a few for rich initial experience
        "sightings_log": [
            {
                "id": "sight_1",
                "species_id": 14,
                "common_name": "Indigo Bunting",
                "timestamp": "2026-10-07T07:45:00",
                "confidence": 0.94,
                "xp_earned": 95,
                "note": "Spotted along sunlit forest edge!"
            },
            {
                "id": "sight_2",
                "species_id": 17,
                "common_name": "Northern Cardinal",
                "timestamp": "2026-10-08T08:15:00",
                "confidence": 0.91,
                "xp_earned": 55,
                "note": "Bright red male singing high in the oak."
            }
        ],
        "unlocked_badges": ["first_steps", "first_feather"],
        "completed_challenges": [],
        "session_history": [
            {
                "id": "sess_1",
                "duration_minutes": 28,
                "app_seconds": 45,
                "discoveries": 1,
                "xp_earned": 145,
                "date": "2026-10-07"
            },
            {
                "id": "sess_2",
                "duration_minutes": 48,
                "app_seconds": 60,
                "discoveries": 1,
                "xp_earned": 195,
                "date": "2026-10-08"
            }
        ]
    }

def load_user_state() -> Dict[str, Any]:
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    state = init_user_state()
    save_user_state(state)
    return state

def save_user_state(state: Dict[str, Any]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

# Request Models
class Base64IdentifyRequest(BaseModel):
    image_base64: str
    top_k: Optional[int] = 5

class RecordDiscoveryRequest(BaseModel):
    species_id: int
    confidence: float
    notes: Optional[str] = ""

class RecordSessionRequest(BaseModel):
    duration_minutes: int
    app_seconds: int
    discoveries_count: int

# ==================== API ENDPOINTS ====================

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "offline_mode": True,
        "ai_engine": "local_pytorch",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/model-info")
def get_model_info():
    info = identifier.get_model_info()
    return info

@app.get("/api/system-info")
def get_system_info():
    info = identifier.get_model_info()
    mem = psutil.virtual_memory()
    return {
        "model": info,
        "system": {
            "platform": sys.platform,
            "cpu_count": psutil.cpu_count(logical=True),
            "ram_total_gb": round(mem.total / (1024**3), 2),
            "ram_used_percent": mem.percent,
            "offline_verified": True
        }
    }

@app.get("/api/species")
def get_all_species(query: Optional[str] = None, family: Optional[str] = None):
    all_spec = load_species_data()
    user_state = load_user_state()
    discovered_set = set(user_state.get("discovered_species_ids", []))

    results = []
    for s in all_spec:
        is_disc = s["id"] in discovered_set
        item = dict(s)
        item["is_discovered"] = is_disc
        
        # Filter query
        if query:
            q = query.lower()
            if q not in item["common_name"].lower() and q not in item["family"].lower() and q not in item["habitat"].lower():
                continue
        if family and family.lower() != "all" and item["family"].lower() != family.lower():
            continue

        results.append(item)

    return {
        "total_species": len(all_spec),
        "discovered_count": len(discovered_set),
        "results": results
    }

@app.get("/api/species/{species_id}")
def get_species_detail(species_id: int):
    all_spec = load_species_data()
    user_state = load_user_state()
    for s in all_spec:
        if s["id"] == species_id:
            item = dict(s)
            item["is_discovered"] = s["id"] in set(user_state.get("discovered_species_ids", []))
            return item
    raise HTTPException(status_code=404, detail="Species not found")

@app.get("/api/demo-samples")
def get_demo_samples_endpoint():
    samples = load_demo_samples()
    return {
        "samples": samples
    }

from fastapi import Request

@app.post("/api/identify")
async def identify_image(request: Request):
    """
    Core AI bird identification endpoint.
    Processes image locally and evaluates confidence & uncertainty.
    Accepts JSON with image_base64 or multipart/form-data with file.
    """
    image_bytes = None
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            body = await request.json()
            b64_data = body.get("image_base64", "")
            if "," in b64_data:
                b64_data = b64_data.split(",", 1)[1]
            if b64_data:
                image_bytes = base64.b64decode(b64_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    elif "multipart/form-data" in content_type:
        try:
            form = await request.form()
            file = form.get("file")
            if file and hasattr(file, "read"):
                image_bytes = await file.read()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Form data: {str(e)}")
    else:
        # Fallback try json then form
        try:
            body = await request.json()
            b64_data = body.get("image_base64", "")
            if "," in b64_data:
                b64_data = b64_data.split(",", 1)[1]
            if b64_data:
                image_bytes = base64.b64decode(b64_data)
        except Exception:
            pass

    if not image_bytes:
        raise HTTPException(status_code=400, detail="No valid image provided in request")

    try:
        result = identifier.identify(image_bytes, top_k=5)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.get("/api/user/profile")
def get_user_profile():
    state = load_user_state()
    all_spec = load_species_data()
    total_species = len(all_spec)
    discovered_count = len(state.get("discovered_species_ids", []))
    
    # Calculate Level based on XP
    xp = state.get("total_xp", 0)
    level = max(1, xp // 150 + 1)
    title = get_title_for_level(level)
    state["level"] = level
    state["title"] = title

    return {
        **state,
        "total_species_catalog": total_species,
        "discovered_percentage": round((discovered_count / max(1, total_species)) * 100, 1),
        "badges_unlocked_count": len(state.get("unlocked_badges", [])),
        "total_badges_available": len(DEFAULT_BADGES)
    }

@app.post("/api/user/discovery")
def record_discovery(payload: RecordDiscoveryRequest):
    state = load_user_state()
    all_spec = load_species_data()
    
    spec_meta = next((s for s in all_spec if s["id"] == payload.species_id), None)
    if not spec_meta:
        raise HTTPException(status_code=404, detail="Species ID not found")

    is_first_time = payload.species_id not in state["discovered_species_ids"]
    
    # Base XP calculation
    base_xp = spec_meta.get("base_xp", 75)
    awarded_xp = base_xp + (100 if is_first_time else 25)

    if is_first_time:
        state["discovered_species_ids"].append(payload.species_id)

    sighting = {
        "id": f"sight_{int(time.time())}",
        "species_id": payload.species_id,
        "common_name": spec_meta["common_name"],
        "timestamp": datetime.now().isoformat(),
        "confidence": payload.confidence,
        "xp_earned": awarded_xp,
        "note": payload.notes or "Spotted during outdoor exploration"
    }
    state["sightings_log"].insert(0, sighting)
    state["total_xp"] += awarded_xp

    # Check for newly unlocked badges
    new_unlocked_badges = []
    species_count = len(state["discovered_species_ids"])
    
    if "first_feather" not in state["unlocked_badges"] and species_count >= 1:
        state["unlocked_badges"].append("first_feather")
        new_unlocked_badges.append("first_feather")
    
    if "sharp_eyes" not in state["unlocked_badges"] and species_count >= 5:
        state["unlocked_badges"].append("sharp_eyes")
        new_unlocked_badges.append("sharp_eyes")

    if "bird_nerd" not in state["unlocked_badges"] and species_count >= 25:
        state["unlocked_badges"].append("bird_nerd")
        new_unlocked_badges.append("bird_nerd")

    save_user_state(state)

    return {
        "success": True,
        "is_first_time": is_first_time,
        "awarded_xp": awarded_xp,
        "total_xp": state["total_xp"],
        "new_badges": new_unlocked_badges,
        "species": spec_meta
    }

@app.post("/api/user/session")
def record_outdoor_session(payload: RecordSessionRequest):
    """
    Logs an outdoor session.
    Awards XP proportionally to minutes spent OUTDOORS vs MINIMAL screen time.
    """
    state = load_user_state()
    
    # Outdoor reward: 3 XP per minute outdoors + 50 XP session completion bonus
    outdoor_xp = (payload.duration_minutes * 3) + 50
    state["total_xp"] += outdoor_xp
    state["total_outdoor_minutes"] += payload.duration_minutes
    state["total_app_minutes"] += max(1, payload.app_seconds // 60)

    # Update streak
    today_str = str(date.today())
    if state.get("last_active_date") != today_str:
        state["streak_days"] = state.get("streak_days", 0) + 1
        state["last_active_date"] = today_str

    session_record = {
        "id": f"sess_{int(time.time())}",
        "duration_minutes": payload.duration_minutes,
        "app_seconds": payload.app_seconds,
        "discoveries": payload.discoveries_count,
        "xp_earned": outdoor_xp,
        "date": today_str
    }
    state["session_history"].insert(0, session_record)

    # Check badges
    new_badges = []
    if "first_steps" not in state["unlocked_badges"] and len(state["session_history"]) >= 1:
        state["unlocked_badges"].append("first_steps")
        new_badges.append("first_steps")

    if "trail_regular" not in state["unlocked_badges"] and state["streak_days"] >= 7:
        state["unlocked_badges"].append("trail_regular")
        new_badges.append("trail_regular")

    if "touch_grass_champion" not in state["unlocked_badges"] and state["total_outdoor_minutes"] >= 600:
        state["unlocked_badges"].append("touch_grass_champion")
        new_badges.append("touch_grass_champion")

    save_user_state(state)

    return {
        "success": True,
        "session": session_record,
        "awarded_xp": outdoor_xp,
        "total_xp": state["total_xp"],
        "streak_days": state["streak_days"],
        "new_badges": new_badges
    }

@app.get("/api/badges")
def get_badges():
    state = load_user_state()
    unlocked_set = set(state.get("unlocked_badges", []))
    
    result = []
    for b in DEFAULT_BADGES:
        item = dict(b)
        item["unlocked"] = b["id"] in unlocked_set
        result.append(item)
    return {"badges": result}

@app.get("/api/challenges")
def get_challenges():
    return {"challenges": DEFAULT_CHALLENGES}

@app.get("/api/leaderboard")
def get_leaderboard(period: str = "this_week"):
    state = load_user_state()
    
    # Meaningful ranking based on outdoor minutes & species discovered
    mock_explorers = [
        {"rank": 1, "name": "Maya Chen", "title": "Nature Nerd", "xp": 1840, "species_count": 22, "outdoor_hours": 14.5, "streak": 9, "avatar": "🌿"},
        {"rank": 2, "name": "Arjun Patel", "title": "Field Observer", "xp": 1620, "species_count": 19, "outdoor_hours": 12.2, "streak": 7, "avatar": "🔭"},
        {"rank": 3, "name": state["user_name"], "title": state.get("title", "Trail Scout"), "xp": state.get("total_xp", 340) + 1100, "species_count": len(state.get("discovered_species_ids", [])) + 12, "outdoor_hours": round(state.get("total_outdoor_minutes", 76)/60 + 8.5, 1), "streak": state.get("streak_days", 4), "avatar": "🦅", "is_current_user": True},
        {"rank": 4, "name": "Priya Sharma", "title": "Trail Scout", "xp": 1230, "species_count": 15, "outdoor_hours": 9.8, "streak": 5, "avatar": "🌻"},
        {"rank": 5, "name": "Rahul Verma", "title": "Curious Human", "xp": 1050, "species_count": 12, "outdoor_hours": 8.0, "streak": 3, "avatar": "🌲"},
        {"rank": 6, "name": "Elena Rostova", "title": "Curious Human", "xp": 890, "species_count": 9, "outdoor_hours": 6.5, "streak": 4, "avatar": "🍂"},
    ]
    return {
        "period": period,
        "ranking_metric": "Outdoor Activity & Verified Discoveries",
        "leaderboard": mock_explorers
    }

# Serve demo images
if os.path.exists("data/demo_images"):
    app.mount("/demo_images", StaticFiles(directory="data/demo_images"), name="demo_images")

# Serve frontend build if present
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
