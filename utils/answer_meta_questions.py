# utils/answer_meta_questions.py
import re
import unicodedata
import streamlit as st

def normalize(text: str) -> str:
    """Text vereinheitlichen: Unicode, lowercase, trim, Quotes + Satzzeichen entfernen."""
    t = unicodedata.normalize("NFKC", text or "").lower().strip()
    t = re.sub(r"[„“\"'’`´]", "", t)
    t = re.sub(r"[?.!,:;()\[\]{}]", " ", t)
    return re.sub(r"\s+", " ", t)

def reply(text: str):
    """Assistentenantwort speichern."""
    st.session_state.history.append({"role": "assistant", "content": text})

def is_greeting(text: str) -> bool:
    """Prüfen: Begrüßung oder Identitätsfrage?"""
    greet = r"(hallo|hi|hey|moin|servus|guten (tag|morgen|abend))\s*"
    ident = ["wer bist du", "wie heißt du", "wie heisst du", "wer sind sie"]
    return re.fullmatch(greet, text) or any(k in text for k in ident)

def is_capability(text: str) -> bool:
    """Prüfen: Frage nach Fähigkeiten?"""
    keys = [
        "wie kannst du mir helfen", "was kannst du tun", "wobei kannst du helfen",
        "was machst du", "was kannst du mir hilfreich"
    ]
    return any(k in text for k in keys)

def answer_meta_questions(q: str) -> bool:
    """Meta-Fragen erkennen und beantworten."""
    q = normalize(q)

    if is_greeting(q):
        reply(
            "Hallo! 😊 Ich bin dein Nachhaltigkeits-Assistent. "
            "Ich unterstütze dich bei der Analyse von Nachhaltigkeitsberichten sowie bei der Entwicklung von Ideen, "
            "um die Nachhaltigkeitsstrategie deines Unternehmens zu verbessern.\n\n"
            "Ich kann dir helfen mit:\n"
            "- Maßnahmen zur Verbesserung der ESG-Leistung\n"
            "- Branchenbezogenen Best Practices\n"
            "- Analyse von Stärken und Schwächen in Berichten\n"
            "- Konkreten Handlungsempfehlungen\n"
            "- Bewertung von Struktur, Transparenz und Glaubwürdigkeit der Berichterstattung\n\n"
            "Womit möchtest du starten?"
        )
        return True

    if is_capability(q):
        reply(
            "Ich helfe dir dabei, Nachhaltigkeitsstrategien und -berichte gezielt zu verbessern. 🌱\n"
            "- Analyse der Inhalte von Nachhaltigkeitsberichten\n"
            "- Identifikation von Verbesserungspotenzialen\n"
            "- Entwicklung von Maßnahmen und KPIs\n"
            "- Branchenbeispiele und Best Practices\n"
            "- Unterstützung bei Struktur, Sprache und Transparenz\n\n"
            "Sag mir einfach, ob du eine **Analyse, Ideen oder Empfehlungen** brauchst."
        )
        return True

    return False # Es ist keine Metafrage.
