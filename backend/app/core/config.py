# backend/app/core/config.py
"""
Simple config for the backend. Doesn't require pydantic.
Reads configuration from environment variables with defaults.
"""

import os
from pathlib import Path
from typing import Optional

# Base directory of repository (optional, adjust if needed)
BASE_DIR = Path(__file__).resolve().parents[2]

def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    val = os.getenv(name)
    if val is not None:
        return val
    return default

class Settings:
    # Data directory where skills JSON, etc. is stored
    DATA_DIR: str = _env("DATA_DIR", str(BASE_DIR / "data"))
    SKILLS_FILE: str = _env("SKILLS_FILE", "skills_master.json")

    # Database / external services (if/when you add them)
    MONGO_URI: str = _env("MONGO_URI", "mongodb://localhost:27017")
    NEO4J_URI: str = _env("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = _env("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = _env("NEO4J_PASSWORD", "password")

    # other settings
    HOST: str = _env("HOST", "127.0.0.1")
    PORT: int = int(_env("PORT", "8000"))

# single settings instance to import elsewhere
settings = Settings()
