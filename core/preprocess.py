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
PATH_RAW         = Path(os.getenv("PATH_RAW"))
PATH_UPLOAD      = Path(os.getenv("PATH_UPLOAD"))
PATH_PROCESSING  = Path(os.getenv("PATH_PROCESSING"))
PATH_PROCESSED   = Path(os.getenv("PATH_PROCESSED"))
PATH_DB          = Path(os.getenv("PATH_DB"))

# Verzeichnisse sicherstellen
for folder in (PATH_RAW, PATH_UPLOAD, PATH_PROCESSING, PATH_PROCESSED, PATH_DB):
    folder.mkdir(parents=True, exist_ok=True)