# core/retrieval.py
import time
from chromadb.config import Settings

from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from langchain.chains import ConversationalRetrievalChain

from core.preprocess import * # Alle globale Variablen & .env-Variablen stecken hier

from utils.next_neighbor_retriever import NextNeighborRetriever
from utils.ollama_embed import OllamaEmbeddings
from utils.logger import logger

logger.info("------------------------------------------------------------ START retrieval.py")

# --- Kette bauen ---
def get_chain():

    logger.info("Erzeuge neue Retrieval-Kette (Embeddings + Chroma + LLM).")

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
    llm = ChatOllama(model=LLM_MODEL, base_url=os.getenv("OLLAMA_URL"))

    # 5) Prompt
    prompt = PromptTemplate.from_template("""
        Du bist ein Support-Chatbot, der Unternehmen bei der Analyse und Verbesserung ihrer Nachhaltigkeitsberichte unterstützt.
        Deine Aufgabe ist es, auf deutsch, faktenbasiert und präzise auf Fragen zu antworten. Dabei darfst du nur den bereitgestellten Kontext und den letzten Chatverlauf nutzen.        Wenn der Chatverlauf für die Frage nicht relevant ist, ignoriere ihn und befolge ausschließlich die oben genannten Regeln.
        Wenn kein Kontext vorhanden ist, antworte: 'Information nicht gefunden. Bitte versuche es mit einer anderen Frage.'
            
        Chatverlauf (letzte Turns):
        {chat_history}
    
        Kontext:
        {context}
    
        Nutzerfrage:
        {question}
    """)

    # 6) Retrieval-QA-Kette
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    logger.info("Retrieval-Kette erfolgreich erstellt.")
    return chain

#--------------------------------------------------------------------------------------------------------------------
# Antwort generieren
def answer(q: str, chat_history: list[tuple[str, str]]):
    try:
        chat_history = chat_history [-5:] # nur die letzten 5 Runden behalten
        logger.info(f"Neue Frage: \"{q}\", Chat-History-Länge: {len(chat_history)}")
        time.perf_counter(); tmp_time = time.perf_counter()
        out = get_chain().invoke({"question": q, "chat_history": chat_history})
        logger.info(f"Antwort erzeugt in  {((time.perf_counter() - tmp_time) * 1000)/1000:.1f} s")

        # Quelle(n) anzeigen
        print("\n--- Gefundene Chunks ---")
        for i, doc in enumerate(out["source_documents"], 1):
            print(f"Chunk [{i}], Quelle: {doc.metadata.get('source')}, Länge: {len(doc.page_content)}")
            print(doc.page_content, "\n")
            print("\n---\n")
        print("\n--- Ende der Chunks. ---")

        return out["answer"]

    except Exception:
        logger.exception(f"⚠️ Fehler in answer() -Methode in retrieval.py bei der Frage: \"{q}\"")
        return "⚠️ Fehler: Anfrage konnte nicht verarbeitet werden."

if __name__ == "__main__":
    print()

""" # Endlose Schleife
frage = " zusätzliche Instanzen"
while True:
    result = answer(frage)
    # print(result)  
"""