# main.py
import streamlit as st
from core.retrieval import answer
from utils.handle_meta_questions import handle_meta_questions
import threading, time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.preprocess import UPLOAD_PATH 
from core.ingestion import ingestion

# -------------------------------------------------------------------------------------------------------
# Style
st.set_page_config(page_title="RAG-BOT", layout="centered")
st.title("RAG-BOT")
st.caption("Willkommen bei deinem RAG-BOT")
st.sidebar.subheader("Chat-Verlauf")

# -------------------------------------------------------------------------------------------------------
# Auto-Index: Watchdog (neue Dateien in /upload automatisch indexieren – ohne Typ-Filter)
_DEBOUNCE_SEC = 1.0             # Entprellung/Bündelung mehrerer Events
_kick_timer = None
_kick_lock = threading.Lock()

def _count_upload_files():
    p = Path(UPLOAD_PATH)
    count = sum(1 for f in p.glob("*") if f.is_file())
    print(f"[INFO] Aktuell {count} Datei(en) im Upload-Ordner erkannt.")
    return count

def _maybe_run():
    count = _count_upload_files()
    if count > 0:
        print(f"[WATCHDOG] {count} neue Datei(en) gefunden → Ingestion wird gestartet ...")
        threading.Thread(target=ingestion, daemon=True).start()
    else:
        print("[WATCHDOG] Keine neuen Dateien – Ingestion übersprungen.")

def _kick_coalesced():
    global _kick_timer
    with _kick_lock:
        if _kick_timer and _kick_timer.is_alive():
            print("[WATCHDOG] Event erkannt – Timer wird zurückgesetzt (Entprellung aktiv).")
            _kick_timer.cancel()
        else:
            print("[WATCHDOG] Neuer Event erkannt – Timer gestartet.")
        _kick_timer = threading.Timer(_DEBOUNCE_SEC, _maybe_run)
        _kick_timer.daemon = True
        _kick_timer.start()

class _Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type in ("deleted", "moved"):
            print(f"[WATCHDOG] Datei gelöscht/verschoben: {event.src_path} – keine Aktion.")
            return
        print(f"[WATCHDOG] Änderung erkannt: {event.src_path} ({event.event_type})")
        _kick_coalesced()

def _start_watcher():
    obs = Observer()
    obs.schedule(_Handler(), str(Path(UPLOAD_PATH)), recursive=False)
    obs.daemon = True
    obs.start()
    return obs

# Watchdog immer aktiv
if "watchdog_started" not in st.session_state:
    print("[INIT] Watchdog war nicht aktiv – wird jetzt gestartet ...")
    _start_watcher()
    st.session_state["watchdog_started"] = True
else:
    print("[INIT] Watchdog läuft bereits.")

# -------------------------------------------------------------------------------------------------------
# Beim Start prüfen, ob Dateien vorhanden sind
initial_count = sum(1 for f in Path(UPLOAD_PATH).glob("*") if f.is_file())
if initial_count > 0:
    print(f"❗ Beim Start {initial_count} Datei(en) im Upload-Ordner gefunden → Ingestion wird gestartet ...")
    threading.Thread(target=ingestion, daemon=True).start()
    print("✅ Initiale Ingestion ausgelöst.")
else:
    print("[INIT] Upload-Ordner ist leer – keine Ingestion nötig.\n\n\n")

# -------------------------------------------------------------------------------------------------------
# Chat-Verlauf im Session State halten
if "history" not in st.session_state:
    st.session_state.history = []       # speichert alte Nachrichten [{"role": "user"/"assistant", "content": "..."}]

def last_turns(n=5):
    # in (user, assistan)-tupel umwandlen
    pairs, cur = [], []
    for turn in st.session_state.history:
        if turn["role"] == "user":
            cur = [turn["content"], ""]
        else:
            if cur:
                cur[1] = turn["content"]
                pairs.append(tuple(cur))
                cur = []
    return pairs[-n:]

# -------------------------------------------------------------------------------------------------------
# Eingabe
col1, col2 = st.columns([4,1])
with col1: user_q = st.text_input("Frage eingeben", value="", placeholder="Stelle deine Frage ...")
with col2: ask    = st.button("↑")

# -------------------------------------------------------------------------------------------------------
# Anfragen (+ Speichern)
if ask and user_q.strip(): # '.strip()' entfernt Leerzeichen am Anfang und Ende.a
    st.session_state.history.append({"role": "user", "content": user_q}) # '.append()' fügt neues Element am Ende der Liste
    st.session_state.history = st.session_state.history[-200:] # Verlauf nie über 200 Nachrichten wächst.

    # 1) Meta-Fragen lokal beantworten
    if handle_meta_questions(user_q):
        pass  # nichts weiter tun
    else:
        with st.spinner("Thinking …"):
            try:
                chat_hist = last_turns(n=5)       # nur die letzten 5 Turns (Liste mit User–Bot-Paare) herausholen
                resp = answer(user_q, chat_hist)  # <— chat_history wird genutzt
            except Exception as e:
                resp = f"Fehler: {e}"
        st.session_state.history.append({"role": "assistant", "content": resp})
        st.session_state.history = st.session_state.history[-200:]  # Verlauf nie über 200 Nachrichten wächst.

# -------------------------------------------------------------------------------------------------------
# Chatverlauf anzeigen
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])