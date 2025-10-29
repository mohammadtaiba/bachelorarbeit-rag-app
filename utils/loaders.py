# utils/loaders.py
from langchain.schema import Document
from typing import List
from core.config import MARKDOWN_TEMP_DIR
from langchain_community.document_loaders import TextLoader

# --- Markdown-Dateien laden ---
def load_docs() -> List[Document]:
    print("Lade Markdown-Dokumente ...")
    docs: List[Document] = []
    for md in sorted(MARKDOWN_TEMP_DIR.glob("*.md")):
        docs.extend(TextLoader(str(md), encoding="utf-8").load())
    return docs
