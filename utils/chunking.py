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
        chunk_size=2000,
        chunk_overlap=300,
        separators=[
            "\n\n",                 # Absatz
            "\n",                   # Zeile / Listen / Markdown
            "\n- ", "\n* ",         # Bullet-Listen
            "! ", "? ",             # Satzenden
            ". ",                   # Satzende
            "* ",                   # Bullet-Liste
            "; ", "– ", ", ",       # Trennzeichen
            " ",                    # Wort
            "",                     # Fallback
        ]
    )

    chunks = []

    for doc in docs:
        raw_src = doc.metadata.get("source", "")
        src_clean = clean_name(Path(raw_src).stem)

        filename = Path(raw_src).name
        suffix = f"\n\n---\nQuelle: {filename}\n" # Am Ende indexieren

        # ---------------------------------------------------------
        # MarkdownHeaderTextSplitter, wenn Dateiname mit "dnk_datei_" anfängt
        # -> zusätzlich per RecursiveCharacterTextSplitter begrenzen
        # ---------------------------------------------------------
        if Path(raw_src).stem.startswith("dnk_datei_"):
            parts = markdownHeaderTextSplitter.split_text(doc.page_content or "")
            for part in parts:
                # part ist ein Document mit page_content + Header-Metadaten
                for chunk in recursiveCharacterTextSplitter.split_documents([part]):
                    chunk.metadata = {
                        "source": src_clean,
                        **chunk.metadata,  # enthält die Header (H1/H2/H3) vom part
                    }
                    chunk.page_content = chunk.page_content.rstrip() + suffix
                    chunks.append(chunk)

        # ---------------------------------------------------------
        # Sonst → RecursiveCharacterTextSplitter
        # ---------------------------------------------------------
        else:
            for chunk in recursiveCharacterTextSplitter.split_documents([doc]):
                chunk.metadata = {"source": src_clean }
                chunk.page_content = chunk.page_content.rstrip() + suffix
                chunks.append(chunk)

    # ---------------------------------------------------------
    # Chunking-Größe ausgeben
    # ---------------------------------------------------------
    if chunks:
        sizes = [len(c.page_content or "") for c in chunks]
        logger.info(
            "Chunking abgeschlossen (Chunks: %d | Min: %d | Max: %d | Avg: %.1f).",
            len(chunks), min(sizes), max(sizes), sum(sizes) / len(sizes)
        )
    else:
        logger.info("Chunking abgeschlossen (Chunks: 0).")
    return chunks
