"""
Simple config for the backend. Doesn't require pydantic.
Reads configuration from environment variables with defaults.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env from backend/ directory
load_dotenv()

# Base directory of repository (optional, adjust if needed)
BASE_DIR = Path(__file__).resolve().parents[2]


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value is not None else default


class Settings:
    def __init__(self):
        # Keys from .env
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.MONGO_URI = os.getenv("MONGO_URI")
        # Data paths
        self.DATA_DIR = _env("DATA_DIR", str(BASE_DIR / "data"))
        self.SKILLS_FILE = _env("SKILLS_FILE", "skills_master.json")

        # Database / external services
        self.MONGO_URI = _env("MONGO_URI", "mongodb://localhost:27017")
        self.NEO4J_URI = _env("NEO4J_URI", "bolt://localhost:7687")
        self.NEO4J_USER = _env("NEO4J_USER", "neo4j")
        self.NEO4J_PASSWORD = _env("NEO4J_PASSWORD", "password")

        # Server defaults
        self.HOST = _env("HOST", "127.0.0.1")
        self.PORT = int(_env("PORT", "8000"))


# single settings instance to import elsewhere
settings = Settings()
