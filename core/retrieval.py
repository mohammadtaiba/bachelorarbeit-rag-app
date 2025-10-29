# core/retrieval.py
# Chroma laden → Retriever → LM-Studio-LLM → QA

import time
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from chromadb.config import Settings
from langchain_openai import ChatOpenAI
from utils.lmstudio_embed import LMStudioEmbeddings
from core.config import * # Alle globale Variablen & .env-Variablen stecken hier



# --- Kette bauen ---
def get_chain():

    embeddings = LMStudioEmbeddings(
        model=EMBED_MODEL,
        base_url=LMSTUDIO_URL,
        api_key=LMSTUDIO_API_KEY,
    )

    # 2) Vektor-DB verbinden
    vectordb = Chroma(
        collection_name=COLLECTION,
        persist_directory=DB_DIR,
        embedding_function=embeddings,
        client_settings=Settings(anonymized_telemetry=False),
    )

    # 3) Retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 8})

    # 4) LLM
    llm = ChatOpenAI(
        model=LLM_MODEL,
        base_url=LMSTUDIO_URL,
        api_key=LMSTUDIO_API_KEY,
    )

    # 5) Prompt
    prompt = PromptTemplate.from_template(
        """
        Du bist ein Schulpersonal-Assistent, der Fragen zu offiziellen LUSD-Unterlagen beantwortet. 
        Antworte nur aus bereitgestelltem Kontext; sonst: ‘Keine Kontext gefunden.’. 
        Kontext:
        {context}

        Frage:
        {question}

        Antworte vollständig und sachlich auf die Frage (genau von dem Kontext antwroten!).
        """
    )

    # 6) Retrieval-QA-Kette
    a = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    return a

# --- API ---
start_time = time.perf_counter() # Laufzeitmessen
def answer(q: str) -> str:
    chain = get_chain()
    tmp_time = time.perf_counter()
    out = chain.invoke({"query": q})
    print(f"invoke-Laufzeit: {(time.perf_counter() - tmp_time) * 1000:.0f} ms")

    # Quelle(n) anzeigen
    print("\n--- Gefundene Chunks ---")
    for i, doc in enumerate(out["source_documents"], 1):
        print(f"Chunk [{i}], Quelle: {doc.metadata.get('source')}, Länge: {len(doc.page_content)}")
        print(doc.page_content, "\n")
        print("\n---\n")
    print("\n--- Ende der Chunks. ---")

    return out["result"]

if __name__ == "__main__":
    print()

""" # Schleife
frage = " zusätzliche Instanzen"
while True:
    result = answer(frage)
    # print(result)
"""