# main.py
import streamlit as st
from core.retrieval import answer

# Style
st.set_page_config(page_title="RAG ChatBot", layout="centered")
st.title("RAG ChatBot")
st.caption("Willkommen bei deinem rag2-app")
st.sidebar.subheader("Chat-Verlauf")

# Chat-Verlauf im Session State halten
if "history" not in st.session_state:
    st.session_state.history = []       # speichert alle Nachrichten

# Eingabe
col1, col2 = st.columns([4,1])
with col1: user_q = st.text_input("Frage eingeben", value="", placeholder="Stelle deine Frage ...")
with col2: ask    = st.button("↑")

# Anfragen (+ Speichern)
if ask and user_q.strip(): # '.strip()' entfernt Leerzeichen am Anfang und Ende.
    st.session_state.history.append({"role": "user", "content": user_q}) # '.append()' fügt neues Element am Ende der Liste

    with st.spinner("Suche relevante Stellen …"):
        try:
            resp = answer(user_q)
        except Exception as e:
            resp = f"Fehler: {e}" # Fehler in 'resp' speichern

    st.session_state.history.append({"role": "assistant", "content": resp})

# Chatverlauf anzeigen
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])