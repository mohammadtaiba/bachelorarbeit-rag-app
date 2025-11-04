# utils/lmstudio_embed.py
from langchain_core.embeddings import Embeddings

# Verbindungsschicht zwischen LangChain und LM-Studio.
import requests

class OllamaEmbeddings(Embeddings):
    """LangChain-kompatibles Embedding-Wrapper für lokale Ollama-Instanz."""

    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def embed_documents(self, texts):
        """Mehrere Texte in Embeddings umwandeln."""
        return [self._embed_text(t) for t in texts]

    def embed_query(self, text):
        """Einzelne Query einbetten."""
        return self._embed_text(text)

    def _embed_text(self, text: str):
        """Interne Anfrage an Ollama-API."""
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": self.model, "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]

    print("Das RAG-System ist jetzt mit LMStudio verbunden.")