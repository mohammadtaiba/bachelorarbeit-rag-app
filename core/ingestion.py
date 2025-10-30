# core/ingestion.py
from langchain_chroma import Chroma
from chromadb.config import Settings

from utils.lmstudio_embed import LMStudioEmbeddings
from utils.chunking import chunk_documents
from utils.loaders import load_docs
from utils.raw2markdown import convert_all_to_markdown
from utils.cleanup_md import cleanup_md
from utils.file_operation import( convert_doc_to_docx,
                                  delete_doc_files,
                                  move_upload2raw,
                                  move_temp2markdown)
from core.config import * # Alle globale Variablen & .env-Variablen stecken hier

def ingestion():

    if any(Path(UPLOAD_DIR).glob("*")):
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
        chunks = chunk_documents(docs, 900, 90)

        # 5) Embeddings
        embeddings = LMStudioEmbeddings(model=EMBED_MODEL,  base_url=LMSTUDIO_URL, api_key=LMSTUDIO_API_KEY)

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
