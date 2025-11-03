# core/ingestion.py
from pathlib import Path

from langchain_chroma import Chroma
from chromadb.config import Settings
from utils.ollama_embed import OllamaEmbeddings
from utils.chunking import chunk_documents
from utils.loaders import load_docs
from utils.raw2markdown import convert_all_to_markdown
from utils.cleanup_md import cleanup_md
from utils.file_operation import( convert_doc_to_docx,
                                  delete_doc_files,
                                  move_upload2raw,
                                  move_temp2markdown)
from core.preprocess import *

def ingestion():

    if any(Path(UPLOAD_PATH).glob("*")):
        print("Rohdateien gefunden, starte Ingestion ...")

        # 1) Konvertierung
        convert_doc_to_docx()
        delete_doc_files()
        convert_all_to_markdown()

        # 2) Bereinigung
        cleanup_md()

        # 3) Laden
        docs = load_docs()

        # 4) Chunking
        chunks = chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)

        # 5) Embeddings
        embeddings = OllamaEmbeddings(model=EMBED_MODEL,  base_url=OLLAMA_URL)

        # 6) IN Chroma-DB speichern
        # 6.1) Chroma initialisieren
        vectordb = Chroma(
            collection_name=COLLECTION,
            persist_directory=DB_DIR,
            embedding_function=embeddings,
            client_settings=Settings(anonymized_telemetry=False)
        )

        # 6.2) Alte Chunks der betroffenen Dokumente entfernen (Replace-Strategie)
        affected_docs  = sorted({c.metadata["document_id"] for c in chunks})
        for doc_id in affected_docs:
            vectordb.delete(where={"document_id": doc_id})
        print(f"Alte Einträge gelöscht für: {', '.join(affected_docs) or '-'}")


        # 6.3) in Batches speichern (max-batch-size == 5461) ----
        print("Speichere Chunks in ChromaDB ...")
        BATCH = 2000
        total_chunks = len(chunks)
        for i in range(0, total_chunks, BATCH):
            part = chunks[i:i + BATCH]
            vectordb.add_documents(part)
            print(f"  -> gespeichert: {i + len(part)}/{total_chunks}")
        print("Speicherung abgeschlossen.")

        # 7) Vorbereiten für nächste Ingestion (verschieben)
        move_temp2markdown()
        move_upload2raw()

        print("✅  Ingestion vollständig abgeschlossen.")

    else:
        print(" Achtung: Eine Ingestion findet nicht statt, da es keine neuen Daten zu indexieren gibt!")

if __name__ == "__main__":
    ingestion()
