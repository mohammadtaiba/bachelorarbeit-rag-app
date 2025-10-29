# utils/chunking.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import re

# --- helper: Umlaute normalisieren ---
def normalize_german(text: str) -> str:
    replacements = {
        "ä": "ae", "ö": "oe", "ü": "ue",
        "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
        "ß": "ss"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# --- helper: ID säubern ---
def clean_name(name: str) -> str:
    name = normalize_german(name)
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    return name

# --- Metadaten auf Chunks anwenden (Zähler pro Datei) ---
def add_metadata(chunks):
    counter = {}
    for chunk in chunks:
        src = chunk.metadata.get("source") or chunk.metadata.get("file_path") or chunk.metadata.get("path") or "unknown"
        doc_name = Path(src).stem
        doc_id = clean_name(doc_name)
        counter[doc_id] = counter.get(doc_id, 0) + 1
        chunk.metadata["document_id"] = doc_id
        chunk.metadata["chunk_id"] = f"{doc_id}_{counter[doc_id]}"
    return chunks

# --- Chunking + Metadaten ---
def chunk_documents(docs, chunk_size: int, chunk_overlap: int):
    print("Chunking beginnt ...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    print("Chunking abgeschlossen.")
    return add_metadata(chunks)