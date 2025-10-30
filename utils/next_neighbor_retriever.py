# utils/next_neighbor_retriever.py
from __future__ import annotations
import re
from typing import Any, List, Optional
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun

try:
    # Pydantic v2
    from pydantic import ConfigDict
    _IS_PYD2 = True
except Exception:
    _IS_PYD2 = False


class NextNeighborRetriever(BaseRetriever):
    # --- deklarierte Felder (Pydantic) ---
    base: BaseRetriever
    vectordb: Any
    cap: int = 16

    # --- Pydantic-Konfig ---
    if _IS_PYD2:
        model_config = ConfigDict(arbitrary_types_allowed=True)
    else:
        class Config:
            arbitrary_types_allowed = True

    # ---- Helpers ----
    def _parse_index(self, meta: dict) -> Optional[int]:
        if "chunk_index" in meta:
            try:
                return int(meta["chunk_index"])
            except Exception:
                return None
        cid = meta.get("chunk_id")
        if not cid:
            return None
        m = re.search(r"_(\d+)$", str(cid))
        return int(m.group(1)) if m else None

    def _fetch_next(self, doc: Document) -> Optional[Document]:
        did = doc.metadata.get("document_id")
        idx = self._parse_index(doc.metadata)
        if not did or idx is None:
            return None

        res = self.vectordb._collection.get(
            where={
                "$and": [
                    {"document_id": {"$eq": did}},
                    {"chunk_index": {"$eq": idx + 1}}
                ]
            },
            include=["documents", "metadatas"],
        )
        if res and res.get("documents"):
            return Document(page_content=res["documents"][0],
                            metadata=res["metadatas"][0])

        cid = doc.metadata.get("chunk_id")
        if cid:
            next_id = re.sub(r"_(\d+)$", lambda m: f"_{int(m.group(1))+1}", cid)
            res2 = self.vectordb._collection.get(
                where={"chunk_id": {"$eq": next_id}},
                include=["documents", "metadatas"],
            )
            if res2 and res2.get("documents"):
                return Document(page_content=res2["documents"][0],
                                metadata=res2["metadatas"][0])
        return None

    def _unique(self, docs: List[Document]) -> List[Document]:
        seen = set()
        out: List[Document] = []
        for d in docs:
            key = (d.metadata.get("document_id"), d.metadata.get("chunk_id"))
            if key not in seen:
                seen.add(key); out.append(d)
        return out

    # ---- LangChain 0.3 Hooks ----
    def _get_relevant_documents(
        self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        try:
            hits = self.base.invoke(query)
        except AttributeError:
            hits = self.base.get_relevant_documents(query)
        out: List[Document] = []
        for d in hits:
            out.append(d)
            nxt = self._fetch_next(d)
            if nxt: out.append(nxt)
            if len(out) >= self.cap: break
        return self._unique(out)[:self.cap]

    async def _aget_relevant_documents(
        self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        return self._get_relevant_documents(query, run_manager=run_manager)
