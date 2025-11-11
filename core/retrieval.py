# core/retrieval.py
import time
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from chromadb.config import Settings
from langchain_openai import ChatOpenAI
from utils.ollama_embed import OllamaEmbeddings
from core.preprocess import * # Alle globale Variablen & .env-Variablen stecken hier
from utils.next_neighbor_retriever import NextNeighborRetriever
from langchain.chains import ConversationalRetrievalChain


# --- Kette bauen ---
def get_chain():

    # 1) Embeddingvorberieten
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_URL)

    # 2) Vektor-DB verbinden
    vectordb = Chroma(
        collection_name=COLLECTION,
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        client_settings=Settings(anonymized_telemetry=False),
    )

    # 3) Retriever
    base_retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    retriever = NextNeighborRetriever(base=base_retriever, vectordb=vectordb, cap=10)

    # 4) LLM
    llm = ChatOpenAI(model=LLM_MODEL,base_url=OLLAMA_URL)

    # 5) Prompt
    prompt = PromptTemplate.from_template("""
        Du bist ein Persönlicher-Assistent, der Fragen zu offiziellen RAG-Unterlagen beantwortet.
        Beantworte Fragen sachlich und kurz nur aus dem bereitgestellten Kontext und dem letzten Chatverlauf.
        Antworte nur aus bereitgestelltem Kontext; sonst: ‘Keine Kontext gefunden.’. 
        
        Chatverlauf (letzte Turns):
        {chat_history}
        
        Kontext:
        {context}

        Frage:
        {question}
    """)

    # 6) Retrieval-QA-Kette
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    return chain

# --- API ---
start_time = time.perf_counter() # Laufzeitmessen
def answer(q: str, chat_history: list[tuple[str, str]]):
    chain = get_chain()
    tmp_time = time.perf_counter()
    out = chain.invoke({"question": q, "chat_history": chat_history})
    print(f"invoke-Laufzeit: {(time.perf_counter() - tmp_time) * 1000:.0f} ms")

    """
    # Quelle(n) anzeigen
    print("\n--- Gefundene Chunks ---")
    for i, doc in enumerate(out["source_documents"], 1):
        print(f"Chunk [{i}], Quelle: {doc.metadata.get('source')}, Länge: {len(doc.page_content)}")
        print(doc.page_content, "\n")
        print("\n---\n")
    print("\n--- Ende der Chunks. ---")
    """
    return out["answer"]

if __name__ == "__main__":
    print()

""" # Endlose Schleife
frage = " zusätzliche Instanzen"
while True:
    result = answer(frage)
    # print(result)
"""