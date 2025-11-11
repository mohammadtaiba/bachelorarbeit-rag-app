# core/preprocess.py
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# --- Modelle / API ---
OLLAMA_URL  = os.getenv("OLLAMA_URL")
EMBED_MODEL = os.getenv("EMBED_MODEL")
LLM_MODEL   = os.getenv("LLM_MODEL")
COLLECTION  = os.getenv("COLLECTION")

# --- Pfad-Helper ---
def _as_path(env_key: str) -> Path:
    val = os.getenv(env_key)
    if not val:
        raise RuntimeError(f"Umgebungsvariable {env_key} fehlt.")
    return Path(val)

# --- Datenpfade (zentrales Single-Source-of-Truth) ---
RAW_PATH      = _as_path("DATA_RAW")
UPLOAD_PATH   = _as_path("DATA_UPLOAD")
TEMP_MD_PATH  = _as_path("DATA_TEMP_MD")
FINAL_MD_PATH = _as_path("DATA_MARKDOWN")
DB_PATH       = _as_path("DB_PATH")

# Verzeichnisse EINMALIG sicherstellen
for p in (RAW_PATH, UPLOAD_PATH, TEMP_MD_PATH, FINAL_MD_PATH, DB_PATH):
    p.mkdir(parents=True, exist_ok=True)

# --- Chunking (gemäß Pipelineplan: 512 / 75) ---
def _as_int(env_key: str, default: int) -> int:
    s = os.getenv(env_key)
    try:
        return int(s) if s is not None else default
    except ValueError:
        return default

CHUNK_SIZE    = _as_int("CHUNK_SIZE", 512)
CHUNK_OVERLAP = _as_int("CHUNK_OVERLAP", 75)
