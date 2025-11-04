# main.py
import streamlit as st
from core.retrieval import answer
from utils.handle_meta_questions import handle_meta_questions

# Style
st.set_page_config(page_title="RAG-BOT", layout="centered")
st.title("RAG-BOT")
st.caption("Willkommen bei deinem RAG-BOT")
st.sidebar.subheader("Chat-Verlauf")

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