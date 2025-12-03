# utils/chunking.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from slugify import slugify
from utils.logger import logger

# ======================================================================
# Name normalisieren
# ======================================================================
def clean_name(name: str) -> str:
    return slugify(name)

# ======================================================================
# Metadaten auf Chunks anwenden (Zähler pro Datei)
# ======================================================================
def add_metadata(chunks):
    counter = {}  # zählt pro Dokument die Nummer der Chunks hoch
    for chunk in chunks:
        # Quelle herausfinden, egal wie sie im Metadata heißt
        src = chunk.metadata.get("source") or chunk.metadata.get("file_path") or chunk.metadata.get("path") or "unknown"
        doc_name = Path(src).stem
        doc_id = clean_name(doc_name)
        counter[doc_id] = counter.get(doc_id, 0) + 1
        chunk.metadata["document_id"] = doc_id
        chunk.metadata["chunk_id"] = f"{doc_id}_{counter[doc_id]}"
    return chunks

# ======================================================================
# Chunking + Metadaten
# ======================================================================
def chunk_documents(docs, chunk_size: int, chunk_overlap: int):
    logger.info("Chunking beginnt ...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    logger.info("Chunking abgeschlossen.")
    return add_metadata(chunks)