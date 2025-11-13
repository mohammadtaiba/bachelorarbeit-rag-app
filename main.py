# main.py
import streamlit as st
import threading, time
from pathlib import Path

from core.preprocess import UPLOAD_PATH
from core.ingestion import ingestion
from core.retrieval import answer

from utils.watchdog import start_upload_watcher
from utils.handle_meta_questions import handle_meta_questions
from utils.logger import logger

logger.debug("------------------------------------------------------------ START main.py")  # level=logging.debug?

# -------------------------------------------------------------------------------------------------------
# Style
st.set_page_config(page_title="RAG-BOT", layout="centered")
st.title("RAG-BOT")
st.caption("Willkommen bei deinem RAG-BOT")
st.sidebar.subheader("Chat-Verlauf")

# -------------------------------------------------------------------------------------------------------
# Auto-Index: Watchdog (neue Dateien in /upload automatisch indexieren – ohne Typ-Filter)
def _trigger_ingestion():
    if sum(1 for f in Path(UPLOAD_PATH).glob("*") if f.is_file()) > 0:
        threading.Thread(target=ingestion, daemon=True).start()

if "watchdog_started" not in st.session_state:
    try:
        start_upload_watcher(UPLOAD_PATH, _trigger_ingestion)
        st.session_state["watchdog_started"] = True
        logger.info("Watchdog erfolgreich  gestartet.")
    except Exception as e:
        logger.exception("⚠️ Watchdog konnte nicht gestartet werden.")
else:
    logger.debug("Watchdog läuft bereits.")

# -------------------------------------------------------------------------------------------------------
# Beim Start prüfen, ob Dateien vorhanden sind
initial_count = sum(1 for f in Path(UPLOAD_PATH).glob("*") if f.is_file())
if initial_count > 0:
    logger.info(f"Beim Start {initial_count} Datei(en) gefunden → Initiale Ingestion ausgelöst.")
    threading.Thread(target=ingestion, daemon=True).start()
else:
    logger.debug("Upload-Ordner ist leer – keine Ingestion nötig.")

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