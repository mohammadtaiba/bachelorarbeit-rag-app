# utils/loaders.py
from langchain.schema import Document
from typing import List
from core.preprocess import PATH_PROCESSING
from langchain_community.document_loaders import TextLoader
from utils.logger import logger

# --- Markdown-Dateien laden ---
def load_docs() -> List[Document]:
    logger.info("Lade Markdown-Dokumente ...")
    docs: List[Document] = []
    for md in sorted(PATH_PROCESSING.glob("*.md")):
        docs.extend(TextLoader(str(md), encoding="utf-8").load())
    return docs
