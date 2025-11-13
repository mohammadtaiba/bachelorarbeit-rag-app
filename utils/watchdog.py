# utils/watchdog.py
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from utils.logger import logger

# -------------------------------------------------------------------------------------------------------
# Einstellungen
_DEBOUNCE_SEC = 1.0              # Entprell-Zeit (Sekunden)
_kick_timer = None               # Timer-Objekt
_kick_lock  = threading.Lock()   # Sperre zur Synchronisation

# -------------------------------------------------------------------------------------------------------
# Hauptfunktion: Beobachtet den Upload-Ordner auf Dateiänderungen und ruft on_change() mit Entprellung auf.
def start_upload_watcher(upload_dir: str, on_change: callable) -> Observer:
    def _maybe_run():
        logger.info("WATCHDOG: Entprellzeit abgelaufen → Callback wird ausgeführt.")
        on_change()

    def _kick():
        global _kick_timer
        with _kick_lock:
            if _kick_timer and _kick_timer.is_alive():
                _kick_timer.cancel()
            else:
                logger.info("WATCHDOG: Neuer Event erkannt – Timer gestartet.")
            _kick_timer = threading.Timer(_DEBOUNCE_SEC, _maybe_run)
            _kick_timer.daemon = True
            _kick_timer.start()

    class _Handler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.is_directory:
                return
            if event.event_type in ("deleted", "moved"):
                logger.info(f"WATCHDOG: Datei gelöscht/verschoben: `{event.src_path}` – keine Aktion.")
                return
            _kick()

    obs = Observer()
    obs.schedule(_Handler(), str(Path(upload_dir)), recursive=False)
    obs.daemon = True
    obs.start()
    return obs
