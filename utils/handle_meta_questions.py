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
    if re.fullmatch(r"(hallo|hi|hey|moin|servus|guten (tag|morgen|abend))\s*", q_norm) or \
            any(p in q_norm for p in ["wer bist du", "wie heisst du", "wie heißt du",
                                      "wer sind Sie", "Wie heissen Sie", "wie heißen Sie"]):
        reply_plain(
            "Hallo! 😊 Ich bin dein Nachhaltigkeits-Assistent. "
            "Ich unterstütze dich bei der Analyse von Nachhaltigkeitsberichten und bei der Entwicklung von Ideen "
            "zur Verbesserung der Nachhaltigkeitsstrategie deines Unternehmens.\n\n"
            "Ich kann:\n"
            "- Maßnahmen zur Verbesserung von Umwelt-, Sozial- und Governance-Leistung (ESG) vorschlagen\n"
            "- branchenspezifische Best Practices aufzeigen\n"
            "- Stärken und Schwächen in Berichten erkennen\n"
            "- konkrete Handlungsempfehlungen entwickeln\n"
            "- die Qualität und Struktur der Nachhaltigkeitsberichterstattung bewerten\n\n"
            "Womit möchtest du starten?"
        )
        return True

    if any(p in q_norm for p in ["wie kannst du mir helfen","was kannst du mir hilfreich sein",
                                 "wobei kannst du helfen", "was kannst du tun", "was machst du"]):
        reply_plain(
            "Ich helfe dir, Nachhaltigkeitsstrategien und -berichte gezielt zu verbessern. 🌱\n"
            "- Ich analysiere Inhalte von Nachhaltigkeitsberichten\n"
            "- Ich identifiziere Verbesserungspotenziale bei Strategie, Maßnahmen und KPIs\n"
            "- Ich liefere Ideen und Beispiele aus deiner Branche\n"
            "- Ich unterstütze bei Struktur, Transparenz und Glaubwürdigkeit der Berichterstattung\n"
            "- Ich gebe Feedback zu Sprache, Aufbau und Themenabdeckung\n\n"
            "Sag mir einfach, **ob du eine Analyse, Ideen oder Empfehlungen brauchst** – dann legen wir los."
   )
        return True

    # ===== Letzte / vorletzte Nutzer-Frage/Eingabe/Nachricht =====
    # Beispiele, die gematcht werden:
    # "was war meine letzte Frage", "zeige meine vorletzte eingabe", "was war die letzte nachricht?"
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
