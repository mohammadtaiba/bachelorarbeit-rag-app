# utils/handle_meta_questions.py
import re
import unicodedata
import streamlit as st

def _normalize(text: str) -> str:
    # Kleinbuchstaben, Trim, Unicode-Normalisierung, einfache Satzzeichen raus
    t = unicodedata.normalize("NFKC", text or "")
    t = t.lower().strip()
    t = re.sub(r"[„“\"'’`´]", "", t)            # Anführungen
    t = re.sub(r"[?.!,:;()\[\]{}]", " ", t)     # Satzzeichen
    t = re.sub(r"\s+", " ", t)
    return t

def _get_msgs(role: str):
    return [m["content"] for m in st.session_state.history if m.get("role") == role]

def _get_last_n(role: str, steps_back: int):
    msgs = [m["content"] for m in st.session_state.history if m.get("role") == role]
    return msgs[-steps_back] if len(msgs) >= steps_back else None

def reply_plain(text):
    st.session_state.history.append({"role": "assistant", "content": text})

def handle_meta_questions(q: str) -> bool:
    q_norm = _normalize(q)

    # ===== Identität / Fähigkeiten =====
    if any(p in q_norm for p in ["wer bist du", "wie heisst du", "wie heißt du", "was bist du"]):
        reply_plain("Ich bin ein KI-Assistent für die RAG. Ich helfe bei Fachfragen, Bedienung, Fehlermeldungen, "
                    "Auswertungen, Datenpflege und zeige passende Hilfeseiten oder Schritte an.")
        return True

    if re.fullmatch(r"(hallo|hi|hey|moin|servus|guten (tag|morgen|abend))\s*", q_norm) \
       or re.match(r"^(hallo|hi|hey|moin|servus)\b", q_norm):
        reply_plain(
            "Hallo! 😊 Ich bin dein RAG-Bot und unterstütze dich gerne bei verschiedenen Themen:\n"
            "- Fragen zur RAG-Fachlogik beantworten\n"
            "- Schritt-für-Schritt-Anleitungen in der Anwendung\n"
            "- Relevante Hilfeseiten oder Dokumente finden (RAG)\n"
            "- Fehlermeldungen einordnen & Lösungsvorschläge geben\n"
            "- Formulare/Listen erklären, Felder beschreiben\n"
            "- Zusammenfassungen aus Richtlinien oder Dokus erstellen\n\n"
            "Womit möchtest du starten?"
        )
        return True

    if any(p in q_norm for p in ["wie kannst du mir helfen","was kannst du mir hilfreich sein",
                                 "wobei kannst du helfen", "was kannst du tun", "was machst du"]):
        reply_plain(
            "Ich kann dir bei verschiedenen Themen helfen — je nachdem, was du brauchst. 😊\n"
            "- Fragen zur RAG-Fachlogik beantworten\n"
            "- Schritt-für-Schritt-Anleitungen in der Anwendung\n"
            "- Relevante Hilfeseiten/Dokumente finden (RAG)\n"
            "- Fehlermeldungen einordnen & Lösungsvorschläge\n"
            "- Formulare/Listen erklären, Felder validieren (beschreibend)\n"
            "- Zusammenfassungen aus Richtlinien/Dokus\n"
            "\nWenn du magst, sag mir einfach **wobei du gerade Hilfe brauchst**, und ich zeige dir konkret, was ich tun kann."
        )
        return True

    # ===== Letzte / vorletzte Nutzer-Frage/Eingabe/Nachricht =====
    # Beispiele, die gematcht werden:
    # "was war meine letzte frage", "zeige meine vorletzte eingabe", "was war die letzte nachricht?"
    if re.search(r"\bvorletzte(r|n|s)?\b.*\b(frage|eingabe|nachricht)\b", q_norm):
        prev = _get_last_n("user", 2)
        if prev:
            reply_plain(f"Ihre vorletzte Eingabe war: „{prev}“")
        else:
            reply_plain("Kein Kontext gefunden.")
        return True

    if re.search(r"\b(letzte|zuletzt(e|en)?|vorherige)\b.*\b(frage|eingabe|nachricht)\b", q_norm):
        last = _get_last_n("user", 1)
        if last:
            reply_plain(f"Ihre letzte Eingabe war: „{last}“")
        else:
            reply_plain("Kein Kontext gefunden.")
        return True

    # ===== Letzte / vorherige Antwort des Assistenten =====
    # Beispiele: "was war deine letzte antwort", "zeige vorherige antwort"
    if re.search(r"\b(letzte|vorherige)\b.*\b(antwort|reply)\b", q_norm):
        last_a = _get_last_n("assistant", 1)
        if last_a:
            reply_plain(f"Meine letzte Antwort war: „{last_a}“")
        else:
            reply_plain("Ich finde keine vorherige Antwort im Verlauf.")
        return True

    # ===== Fallback: nichts von oben =====
    return False
