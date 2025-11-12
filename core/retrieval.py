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
    llm = ChatOpenAI(
        model=LLM_MODEL,
        base_url=f"{os.getenv('OLLAMA_URL')}/v1",
        api_key="ollama")

    # 5) Prompt
    prompt = PromptTemplate.from_templateprompt = PromptTemplate.from_template("""
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
    return chain

#--------------------------------------------------------------------------------------------------------------------
# Antwort generieren
def answer(q: str, chat_history: list[tuple[str, str]]):
    try:
        chat_history = chat_history [-5:] # nur die letzten 5 Runden behalten
        time.perf_counter(); tmp_time = time.perf_counter()
        out = get_chain().invoke({"question": q, "chat_history": chat_history})
        print(f"Chain-Laufzeit: {((time.perf_counter() - tmp_time) * 1000)/1000:.1f} s")

        # Quelle(n) anzeigen
        print("\n--- Gefundene Chunks ---")
        for i, doc in enumerate(out["source_documents"], 1):
            print(f"Chunk [{i}], Quelle: {doc.metadata.get('source')}, Länge: {len(doc.page_content)}")
            print(doc.page_content, "\n")
            print("\n---\n")
        print("\n--- Ende der Chunks. ---")

        return out["answer"]

    except Exception as e:
        print(f"⚠️ Fehler bei \"answer-methode\": {e}")
        return (f"⚠️ Fehler bei \"answer-methode\": {e}")

if __name__ == "__main__":
    print()

""" # Endlose Schleife
frage = " zusätzliche Instanzen"
while True:
    result = answer(frage)
    # print(result)
"""