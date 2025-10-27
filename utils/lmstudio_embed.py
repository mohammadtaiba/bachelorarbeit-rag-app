# utils/lmstudio_embed.py
from langchain_core.embeddings import Embeddings  # Basisklasse (Interface), die LangChain für Embeddings erwartet
from openai import OpenAI                         # Client für HTTP-Anfragen an LM-Studio (OpenAI-kompatible API)
from typing import List


# Diese Klasse ist ein "Wrapper" (= Verbindungsschicht) zwischen LangChain und LM-Studio.
# Sie sagt LangChain, WIE es Embeddings von LM-Studio anfragen kann.
class LMStudioEmbeddings(Embeddings):
    # Konstruktor der Klasse
    def __init__(self, model: str, base_url: str, api_key: str):
        self.model  = model                                       # speichert Modellnamen im Objekt
        self.client = OpenAI(base_url=base_url, api_key=api_key)  # speichern, kapseln, aufbauen Verbindung im Objekt
        self.base_url = base_url
        self.api_key = api_key

    # Wenn LangChain mehrere Texte einbetten will
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        out = []                                                             # Liste für die Embedding-Vektoren
        for t in texts:
            t = t.replace("\n", " ")                             # Zeilenumbrüche entfernen
            resp = self.client.embeddings.create(input=t, model=self.model)  # Anfrage senden → Embedding erzeugen
            out.append(resp.data[0].embedding)                               # Den Vektor aus der Antwort holen
        return out

    # für Nutzer-Anfrage (z. B. die User-Frage)
    def embed_query(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        resp = self.client.embeddings.create(input=text, model=self.model)
        return resp.data[0].embedding                                       # Nur ein Vektor zurückgeben

    print("Das LUSD-System ist jetzt mit LMStudio verbunden.")