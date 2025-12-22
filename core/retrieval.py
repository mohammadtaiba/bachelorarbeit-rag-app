# core/retrieval.py
import time, os
from chromadb.config import Settings

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

from core.preprocess import EMBED_MODEL, OLLAMA_URL, COLLECTION, PATH_DB, LLM_MODEL

from utils.ollama_embed import OllamaEmbeddings
from utils.logger import logger

logger.info("------------------------------------------------------------ START retrieval.py")


# ======================================================================
# Build Conversational Retrieval Chain
# ======================================================================
def build_retrieval_chain():
    """
    Create a conversational retrieval chain consisting of:
        - Embeddings
        - Chroma vector database
        - LLM (ChatOllama)
        - PromptTemplate
    """

    logger.info("Creating new retrieval chain (Embeddings + Chroma + LLM).")

    # ------------------------------------------------------------------
    # Create embedding model
    # ------------------------------------------------------------------
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_URL
    )

    # ------------------------------------------------------------------
    # Connect to vector database
    # ------------------------------------------------------------------
    vector_db = Chroma(
        collection_name=COLLECTION,
        persist_directory=PATH_DB,
        embedding_function=embeddings,
        client_settings=Settings(anonymized_telemetry=False),
    )

    # ------------------------------------------------------------------
    # Create retriever
    # Base retriever first, then wrap with NextNeighborRetriever
    # ------------------------------------------------------------------
    retriever = vector_db.as_retriever(search_kwargs={"k": 40})

    # ------------------------------------------------------------------
    # LLM configuration
    # ------------------------------------------------------------------
    llm = ChatOllama(
        model=LLM_MODEL,
        base_url=os.getenv("OLLAMA_URL"),
        temperature=0.15,
    )

    # ------------------------------------------------------------------
    # Prompt template
    # ------------------------------------------------------------------
    prompt_text = """
        Als hilfreicher KI-Assistent unterstützt du Unternehmen dabei, ihre Nachhaltigkeitsberichte zu analysieren und zu verbessern.
        Deine Aufgabe ist es, Fragen nur aus dem bereitgestellten Kontext auf Deutsch, faktenbasiert und präzise zu beantworten.
        Wenn kein Kontext vorhanden ist, antworte: „Information nicht gefunden.\nBitte versuche es mit einer anderen Frage zum Thema **Nachhaltigkeitsberichte**.”
        Verwende ausschließlich den bereitgestellten Kontext und die letzten Chat-Beiträge.
        Wenn der Chatverlauf nicht relevant ist, ignoriere ihn.
        Ich werde dir Fragen geben und möchte, dass du mir nur die Antwort gibst, ohne viel zu erklären!
            - Schreibe das schön und nur die Antwort ohne Erklärung!
 
        {chat_history}
 
        {context}
 
        {question}
    """

    prompt = PromptTemplate.from_template(prompt_text)

    # ------------------------------------------------------------------
    # Build the conversational retrieval chain
    # ------------------------------------------------------------------
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    logger.info("Retrieval chain successfully created.")
    return chain


BUILD_CHAIN_ONCE = build_retrieval_chain()

# ======================================================================
# Generate Answer
# ======================================================================
def generate_answer(question: str, chat_history: list[tuple[str, str]]):
    """
    Generate an answer using the retrieval chain.
        - Keeps last 5 conversation turns
        - Logs question and timing
        - Returns model answer
        - Prints retrieved chunks for debugging
    """

    try:
        # Keep only last 5 chat pairs
        chat_history = chat_history[-5:]

        logger.info(f"New question received: \"{question}\" | Chat history length: {len(chat_history)}")

        start_time = time.perf_counter()
        output = BUILD_CHAIN_ONCE.invoke({
            "question": question,
            "chat_history": chat_history
        })

        elapsed = (time.perf_counter() - start_time)
        logger.info(f"Answer generated in {elapsed:.2f} seconds")

        # ------------------------------------------------------------------
        # Print source documents for debugging
        # ------------------------------------------------------------------
        print("\n--- Retrieved Chunks ---")
        for i, doc in enumerate(output["source_documents"], start=1):
            print(f"Chunk [{i}] | Source: {doc.metadata.get('source')} | Length: {len(doc.page_content)}")
            print(doc.page_content)
            print("\n---\n")
        print("--- End of Chunks ---\n")

        return output["answer"]

    except Exception:
        logger.exception("⚠️ Error in generate_answer() for question: \"{question}\".")
        return "⚠️ Error: Unable to process the request."


# ======================================================================
if __name__ == "__main__":
    print()
