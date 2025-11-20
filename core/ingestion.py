# core/ingestion.py
import time
from langchain_chroma import Chroma
from chromadb.config import Settings
from pathlib import Path

from utils.logger import logger
from utils.ollama_embed import OllamaEmbeddings
from utils.chunking import chunk_documents
from utils.loaders import load_docs
from utils.raw2markdown import convert_all_to_markdown
from utils.cleanup_md import cleanup_md
from utils.file_operation import( convert_doc_to_docx,
                                  delete_doc_files,
                                  move_upload2raw,
                                  move_temp2markdown)
from core.preprocess import UPLOAD_PATH, EMBED_MODEL, OLLAMA_URL, COLLECTION, DB_PATH
from threading import Lock

_ING_LOCK = Lock()

time.perf_counter(); tmp_time = time.perf_counter()

def ingestion():
    logger.info("------------------------------------------------------------ START ingestion.py")

    # Damit läuft immer nur eine Ingestion
    if not _ING_LOCK.acquire(blocking=False):
        logger.warning("Ingestion läuft bereits - Even ignoriert.")
        return
    try:
        if any(Path(UPLOAD_PATH).glob("*")):
            logger.info("Rohdateien gefunden, starte Ingestion ...")

            # 1) Konvertierung
            convert_doc_to_docx()
            delete_doc_files()
            convert_all_to_markdown()

            # 2) Bereinigung
            cleanup_md()

            # Vorbereiten für nächste Ingestion (verschieben)
            move_upload2raw()

            # 3) Laden
            docs = load_docs()

            # 4) Chunking
            chunks = chunk_documents(docs, 1000, 100)

            # 5) Embeddings
            embeddings = OllamaEmbeddings(model=EMBED_MODEL,  base_url=OLLAMA_URL)

            # 6) IN Chroma-DB speichern
            # 6.1) Chroma initialisieren
            vectordb = Chroma(
                collection_name=COLLECTION,
                persist_directory=DB_PATH,
                embedding_function=embeddings,
                client_settings=Settings(anonymized_telemetry=False)
            )

            # 6.2) Alte Chunks der betroffenen Dokumente entfernen (Replace-Strategie)
            affected_docs  = sorted({c.metadata["document_id"] for c in chunks})
            for doc_id in affected_docs:
                vectordb.delete(where={"document_id": doc_id})
            logger.info(f"Alte Einträge gelöscht für: {', '.join(affected_docs) or '-'}")


            # 6.3) in Batches speichern (max-batch-size == 5461) ----
            logger.info("Speichere Chunks in ChromaDB ...")
            BATCH = 2000
            total_chunks = len(chunks)
            for i in range(0, total_chunks, BATCH):
                part = chunks[i:i + BATCH]
                try:
                    vectordb.add_documents(part)
                except RuntimeError as embed_err:
                    logger.error(f"Embedding-Fehler: {embed_err}")
                    logger.error("🔌 Ingestion abgebrochen, da Ollama nicht erreichbar ist (in Terminal: `ollama serve` ausführen.")
                    return
                logger.info(f"  -> gespeichert: {i + len(part)}/{total_chunks}")
            logger.info("Speicherung abgeschlossen.")

            # Vorbereiten für nächste Ingestion (verschieben)
            move_temp2markdown()

            logger.info("✅  Ingestion vollständig abgeschlossen.")

        else:
            logger.info(" Achtung: Eine Ingestion findet nicht statt, da es keine neuen Daten zu indexieren gibt!")

    except Exception:
        logger.exception("⚠️ Fehler bei der Ingestion.")

    finally:
        _ING_LOCK.release() # gibt den Lock wieder frei

    logger.info(f"Ingestion-Laufzeit: {((time.perf_counter() - tmp_time) * 1000)/1000:.1f} s")

if __name__ == "__main__":
    ingestion()
