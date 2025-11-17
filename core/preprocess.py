# core/preprocess.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Projekt root --> `.env`-datei laden
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# Modelle / API
OLLAMA_URL  = os.getenv("OLLAMA_URL")
EMBED_MODEL = os.getenv("EMBED_MODEL")
LLM_MODEL   = os.getenv("LLM_MODEL")
COLLECTION  = os.getenv("COLLECTION")

# Datenpfade (zentrales Single-Source-of-Truth)
RAW_PATH      = Path(os.getenv("DATA_RAW"))
UPLOAD_PATH   = Path(os.getenv("DATA_UPLOAD"))
TEMP_MD_PATH  = Path(os.getenv("DATA_TEMP_MD"))
FINAL_MD_PATH = Path(os.getenv("DATA_MARKDOWN"))
DB_PATH       = Path(os.getenv("DB_PATH"))

# Verzeichnisse sicherstellen
for folder in (RAW_PATH, UPLOAD_PATH, TEMP_MD_PATH, FINAL_MD_PATH, DB_PATH):
    folder.mkdir(parents=True, exist_ok=True)

# Chunking
CHUNK_SIZE    = os.getenv("CHUNK_SIZE")
CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP")
