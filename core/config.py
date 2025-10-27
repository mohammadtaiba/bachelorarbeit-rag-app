# core/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

# --- .env laden ---
load_dotenv()

# --- Globale-Variablen aus .env ---
LMSTUDIO_URL     = os.getenv("LMSTUDIO_URL")
LMSTUDIO_API_KEY = os.getenv("LMSTUDIO_API_KEY")
EMBED_MODEL      = os.getenv("EMBED_MODEL")
LLM_MODEL        = os.getenv("LLM_MODEL")
COLLECTION       = os.getenv("COLLECTION")

# Globale-Variablen
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

MARKDOWN_DIR = Path("data/markdown")
MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)

DB_DIR = "db/chromadb"
Path(DB_DIR).mkdir(parents=True, exist_ok=True)

