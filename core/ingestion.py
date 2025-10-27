# core/ingestion.py
# PDF → Chunks → Embeddings (LM-Studio) → Chroma
from shutil import rmtree

from langchain_chroma import Chroma
from chromadb.config import Settings

from utils.lmstudio_embed import LMStudioEmbeddings
from utils.chunking import chunk_documents
from utils.loaders import load_docs
from utils.raw2markdown import convert_all_to_markdown
from utils.cleanup_md import cleanup_md
from core.config import * # Alle globale Variablen & .env-Variablen stecken hier

def ingestion():

    # Dokumente-Konvertierung
    if not any(list(MARKDOWN_DIR.glob("*.md")) + list(MARKDOWN_DIR.glob("*.gfm"))):
        print("Keine .md- oder .gfm-Dateien gefunden – Starte Ingestion ...")

        if Path(DB_DIR).exists():
            rmtree(DB_DIR)
            print("Alte ChromaDB gelöscht.")

        # 1) Konvertierung
        convert_all_to_markdown()

        # 2) Bereinigung
        cleanup_md()

        # 3) Laden
        docs = load_docs()

        # 4) Chunking
        chunks = chunk_documents(docs, 512, 75)

        # 5) Embeddings
        embeddings = LMStudioEmbeddings(model=EMBED_MODEL,  base_url=LMSTUDIO_URL, api_key=LMSTUDIO_API_KEY)

        # 6) IN Chroma-DB speichern
        print("Speichere Chunks in ChromaDB ...")
        vectordb = Chroma(
            collection_name=COLLECTION,
            persist_directory=DB_DIR,
            embedding_function=embeddings,
            client_settings=Settings(anonymized_telemetry=False)
        )
        # ---- in Batches speichern (# weil max batch size of 5461, bei viele Chunks == abbruch.) ----
        BATCH = 2000
        total_chunks = len(chunks)
        for i in range(0, total_chunks, BATCH):
            part = chunks[i:i + BATCH]
            vectordb.add_documents(part)
            print(f"  -> gespeichert: {i + len(part)}/{total_chunks}")
        print("Speicherung in ChromaDB abgeschlossen.")
        print("✅  Ingestion vollständig abgeschlossen.")

    else:
        print("Achtung: Die md-Dateien sind da, es findet jetzt keine Ingestion statt!")

if __name__ == "__main__":
    ingestion()
