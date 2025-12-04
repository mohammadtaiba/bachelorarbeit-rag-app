# utils/chunking.py
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from pathlib import Path
from slugify import slugify
from utils.logger import logger

# ======================================================================
# Dateiname normalisieren
# ======================================================================
def clean_name(file_name: str) -> str:
    return slugify(file_name)

# ======================================================================
# Chunking + Metadaten
# ======================================================================
def chunk_documents(docs):
    logger.info("Chunking beginnt ...")

    markdownHeaderTextSplitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "H1"), ("##", "H2"), ("###", "H3")],
        strip_headers=False
    )

    recursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
        chunk_size=3500,
        chunk_overlap=400
    )

    chunks = []

    for doc in docs:
        raw_src = doc.metadata.get("source", "")
        src_clean = clean_name(Path(raw_src).stem)

        # ---------------------------------------------------------
        # MarkdownHeaderTextSplitter, wenn Dateiname mit "dnk_datei_" anfängt
        # ---------------------------------------------------------
        if Path(raw_src).stem.startswith("dnk_datei_"):
            for chunk in markdownHeaderTextSplitter.split_text(doc.page_content):
                chunk.metadata = {
                    "source": src_clean,
                    **chunk.metadata  # alle Headers (H1, H2, H3) aus dem Splitter übernehmen
                }
                chunks.append(chunk)

        # ---------------------------------------------------------
        # Sonst → RecursiveCharacterTextSplitter
        # ---------------------------------------------------------
        else:
            for chunk in recursiveCharacterTextSplitter.split_documents([doc]):
                chunk.metadata = {"source": src_clean }
                chunks.append(chunk)

    logger.info("Chunking abgeschlossen.")
    return chunks
