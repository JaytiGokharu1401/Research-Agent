from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import logging
import uuid
from datetime import datetime
import os
from pathlib import Path

from research.engine import ResearchEngine


logger = logging.getLogger(__name__)

app = FastAPI(title="Research Agent")


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
CONFIGS_DIR = DATA_DIR / "configs"
RESULTS_DIR = DATA_DIR / "results"

CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CONFIGS_PATH = CONFIGS_DIR / "research_configs.json"


# ============================================================
# Research Engine
# ============================================================

research_engine = ResearchEngine(
    results_dir=str(RESULTS_DIR)
)


# ============================================================
# Enable CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Data Models
# ============================================================

class ResearchConfig(BaseModel):
    technology: str
    search_strategy: str
    search_terms: str
    target_audience: str
    timeline_scope: str
    detailed_prompt: Optional[str] = None


# ============================================================
# Helper Functions
# ============================================================

def load_configs():
    """Load all configurations."""

    if not CONFIGS_PATH.exists():
        return []

    with open(CONFIGS_PATH, "r") as f:
        return json.load(f)


def save_configs(configs):
    """Save all configurations."""

    with open(CONFIGS_PATH, "w") as f:
        json.dump(configs, f, indent=2)


def save_config(config: dict):
    """Save single configuration."""

    configs = load_configs()
    configs.append(config)
    save_configs(configs)

    return config


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "Research Agent",
        "status": "running",
        "endpoints": {
            "configs": "/api/v1/configs",
            "docs": "/docs"
        }
    }


# ============================================================
# Configuration Endpoints
# ============================================================

@app.post("/api/v1/configs")
async def create_config(config: ResearchConfig):
    """Create new research configuration and run the research engine."""

    try:
        config_id = str(uuid.uuid4())

        config_data = {
            "id": config_id,
            "technology": config.technology,
            "search_strategy": config.search_strategy,
            "search_terms": config.search_terms,
            "target_audience": config.target_audience,
            "timeline_scope": config.timeline_scope,
            "detailed_prompt": config.detailed_prompt or "",
            "enabled": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "research_status": "starting"
        }

        saved = save_config(config_data)

        # Run research engine
        try:
            print(f"\n{'=' * 60}")
            print(f"STARTING RESEARCH: {config.technology}")
            print(f"{'=' * 60}\n")

            research_results = research_engine.run_and_save(config_data)

            # Save research results
            research_file = RESULTS_DIR / f"{config_id}_research.json"

            with open(research_file, "w") as f:
                json.dump(research_results, f, indent=2)

            print(f"\nResearch saved to: {research_file}\n")

            # Update config with success status
            config_data["research_status"] = "completed"
            config_data["research_id"] = config_id
            config_data["research_file"] = str(
                Path("data") / "results" / f"{config_id}_research.json"
            )

            # Update configs list
            configs = load_configs()

            for i, c in enumerate(configs):
                if c["id"] == config_id:
                    configs[i] = config_data
                    break

            save_configs(configs)

        except Exception as research_error:
            print(f"\nResearch error: {str(research_error)}\n")

            config_data["research_status"] = "error"
            config_data["error_message"] = str(research_error)

        return saved

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.get("/api/v1/configs")
async def get_all_configs():
    """Get all research configurations."""

    try:
        configs = load_configs()

        return {
            "total": len(configs),
            "configs": configs
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/api/v1/configs/{config_id}")
async def get_config(config_id: str):
    """Get specific configuration."""

    try:
        configs = load_configs()

        config = next(
            (c for c in configs if c["id"] == config_id),
            None
        )

        if not config:
            raise HTTPException(
                status_code=404,
                detail="Config not found"
            )

        return config

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.put("/api/v1/configs/{config_id}")
async def update_config(
    config_id: str,
    config: ResearchConfig
):
    """Update configuration."""

    try:
        configs = load_configs()

        idx = next(
            (
                i
                for i, c in enumerate(configs)
                if c["id"] == config_id
            ),
            None
        )

        if idx is None:
            raise HTTPException(
                status_code=404,
                detail="Config not found"
            )

        configs[idx].update({
            "technology": config.technology,
            "search_strategy": config.search_strategy,
            "search_terms": config.search_terms,
            "target_audience": config.target_audience,
            "timeline_scope": config.timeline_scope,
            "detailed_prompt": config.detailed_prompt,
            "updated_at": datetime.now().isoformat()
        })

        save_configs(configs)

        return configs[idx]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.delete("/api/v1/configs/{config_id}")
async def delete_config(config_id: str):
    """Delete configuration."""

    try:
        configs = load_configs()

        configs = [
            c
            for c in configs
            if c["id"] != config_id
        ]

        save_configs(configs)

        return {
            "message": "Config deleted"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# Research Results Endpoints
# ============================================================

@app.get("/api/v1/research/{config_id}")
async def get_research(config_id: str):
    """Get research results for a configuration."""

    try:
        research_file = (
            RESULTS_DIR / f"{config_id}_research.json"
        )

        if not research_file.exists():
            raise HTTPException(
                status_code=404,
                detail="Research not found"
            )

        with open(research_file, "r") as f:
            research_data = json.load(f)

        return research_data

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Research file not found"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/api/v1/research")
async def list_all_research():
    """List all research results."""

    try:
        if not RESULTS_DIR.exists():
            return {
                "total": 0,
                "research": []
            }

        research_files = [
            f
            for f in os.listdir(RESULTS_DIR)
            if f.endswith("_research.json")
        ]

        research_list = []

        for file in research_files:
            try:
                with open(
                    RESULTS_DIR / file,
                    "r"
                ) as f:
                    data = json.load(f)

                    research_list.append({
                        "config_id": data.get("config_id"),
                        "technology": data.get("technology"),
                        "generated_at": data.get("generated_at"),
                        "status": data.get(
                            "status",
                            "completed"
                        )
                    })

            except Exception as e:
                logger.error(
                    f"Error reading {file}: {e}"
                )

        return {
            "total": len(research_list),
            "research": research_list
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )