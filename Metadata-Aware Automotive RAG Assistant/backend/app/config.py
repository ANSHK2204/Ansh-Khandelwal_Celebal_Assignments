"""
Drive Wise - Configuration Module
Centralizes all configuration, paths, and model settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ──────────────────────────────────────────────
# Directory Paths
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
BROCHURES_DIR = BASE_DIR / "brochures"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# Ensure directories exist
BROCHURES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────
# Embedding & Re-ranking Models
# ──────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ──────────────────────────────────────────────
# LLM Configuration (Google Gemini)
# ──────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.1-flash-lite"

# ──────────────────────────────────────────────
# Retrieval Configuration
# ──────────────────────────────────────────────
TOP_K_RETRIEVAL = 10      # Initial vector search results
TOP_N_RERANK = 4          # Final re-ranked results sent to LLM
CHUNK_SIZE = 512          # Max tokens per chunk (fallback chunking)
CHUNK_OVERLAP = 50        # Token overlap between chunks

# ──────────────────────────────────────────────
# ChromaDB Configuration
# ──────────────────────────────────────────────
CHROMA_COLLECTION = "car_brochures"
CHROMA_PERSIST_DIR = str(DATA_DIR / "chromadb")

# ──────────────────────────────────────────────
# Logging Configuration
# ──────────────────────────────────────────────
LOG_DB_PATH = str(LOGS_DIR / "drive_wise.db")
