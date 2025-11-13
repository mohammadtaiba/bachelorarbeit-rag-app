# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ----------------------------------------------------------
# Pfade
ROOT = Path(__file__).resolve().parents[1]

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "rag_bot.log"

# ----------------------------------------------------------
# Logger erstellen
logger = logging.getLogger("rag_bot")
logger.setLevel(logging.INFO)

# ----------------------------------------------------------
# Handler nur einmal hinzufügen
if not logger.handlers:

    # Rotating File Handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,             # 5 alte Logfiles behalten
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

# ----------------------------------------------------------
# Unterdrücke httpx-Spam
logging.getLogger("httpx").setLevel(logging.WARNING)
