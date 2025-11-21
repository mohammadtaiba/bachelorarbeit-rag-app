# main.py
import base64
import threading
from pathlib import Path

import streamlit as st

from utils.handle_meta_questions import handle_meta_questions
from utils.watchdog import start_upload_watcher
from utils.logger import logger

from core.retrieval import generate_answer
from core.preprocess import UPLOAD_PATH
from core.ingestion import ingestion

logger.debug("------------------------------------------------------------ START main.py")


# ======================================================================================================
# Page setup & styling
# ======================================================================================================

def configure_page() -> None:
    """
    Configure basic Streamlit page settings.
    """
    st.set_page_config(
        page_title="RAG-BOT",
        page_icon="utils/assets/logo.svg",
        layout="centered"
    )

    # Header
    st.title("RAG-BOT")
    st.caption("Ideen und Maßnahmen zur Verbesserung von Nachhaltigkeitsstrategien 🌱")


def apply_global_styles() -> None:
    """
    Inject global CSS for sidebar buttons and chat input styling.
    """
    st.markdown(
        """
        <style>
            /* ------------------------------------------- Sidebar --------------------------------------------------- */
            section[data-testid="stSidebar"] button {
                background-color:   inherit !important;     /* button uses same background as sidebar */
                border:             none !important;
                box-shadow:         none !important;
                text-align:         left !important;        /* left-align text */
                justify-content:    flex-start !important;  /* also align icon/text */
                padding-left:       8px !important;         /* slight left padding */
            }

            section[data-testid="stSidebar"] button:hover {
                background-color: rgba(255, 0, 0, 0.25) !important; /* rot */
                transition: background-color 0.2s ease;
            }


            /* ------------------------------------------ Chat input ------------------------------------------------- */        
            div[data-testid="stChatInput"] > div {
                border: 1px !important;
                box-shadow: 0 2px 6px rgba(0,0,0,0.18) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ======================================================================================================
# Sidebar
# ======================================================================================================

def load_logo_base64(logo_path: str = "utils/assets/logo.svg") -> str:
    """
    Load the logo file and return a base64-encoded string.
    If loading fails, an empty string is returned and a warning is logged.
    """
    try:
        logo_bytes = Path(logo_path).read_bytes()
        return base64.b64encode(logo_bytes).decode("utf-8")
    except FileNotFoundError:
        logger.warning("Logo file not found at %s. Sidebar logo will not be displayed.", logo_path)
    except Exception:
        logger.exception("Unexpected error while loading logo file.")
    return ""


def render_sidebar(logo_b64: str) -> None:
    """
    Render the sidebar with logo and 'new chat' button.
    """
    with st.sidebar:
        # ------------------------------------------------------------------------------------------------
        # Clickable logo (links to the same page)
        if logo_b64:
            st.markdown(
                f"""
                 <a href="" style="text-decoration:none;">
                    <img src="data:image/svg+xml;base64,{logo_b64}" width="250" />
                </a>
                """,
                unsafe_allow_html=True,
            )

        st.divider() # separate-line

        # ------------------------------------------------------------------------------------------------
        # Start a new chat session
        if st.button("🗑️ &nbsp;&nbsp; Verlauf", use_container_width=True):
            st.session_state.history = []


# ======================================================================================================
# Ingestion / Watchdog logic
# ======================================================================================================

def upload_directory_contains_files() -> bool:
    """
    Check whether the upload directory currently contains at least one file.
    """
    return any(file_path.is_file() for file_path in Path(UPLOAD_PATH).glob("*"))


def trigger_background_ingestion() -> None:
    """
    Trigger ingestion in a background thread if there are files in the upload directory.
    """
    if upload_directory_contains_files():
        threading.Thread(target=ingestion, daemon=True).start()


def initialize_watchdog() -> None:
    """
    Start the watchdog once per Streamlit session to monitor the upload directory.
    The callback triggers ingestion whenever new files are detected.
    """
    if "watchdog_started" in st.session_state:
        logger.debug("Upload watchdog already running.")
        return

    try:
        start_upload_watcher(UPLOAD_PATH, trigger_background_ingestion)
        st.session_state["watchdog_started"] = True
        logger.info("Upload watchdog successfully started.")
    except Exception:
        logger.exception("Upload watchdog could not be started.")


def trigger_initial_ingestion_if_needed() -> None:
    """
    On app start, check if the upload directory already contains files.
    If so, run an initial ingestion in a background thread.
    """
    file_count = sum(1 for file_path in Path(UPLOAD_PATH).glob("*") if file_path.is_file())
    if file_count > 0:
        logger.info(
            "On startup, %s file(s) found in upload directory -> triggering initial ingestion.",
            file_count,
        )
        threading.Thread(target=ingestion, daemon=True).start()
    else:
        logger.debug("Upload directory is empty – no initial ingestion required.")


# ======================================================================================================
# Chat history helpers
# ======================================================================================================

def ensure_chat_history_initialized() -> None:
    """
    Ensure that the chat history exists in the session state.
    """
    if "history" not in st.session_state:
        # Each message is a dict: {"role": "user" | "assistant", "content": "..."}
        st.session_state.history = []


def get_recent_chat_turn_pairs(limit: int = 5) -> list[tuple[str, str]]:
    """
    Convert the flat message list into user/assistant pairs and return the last `limit` pairs.

    This structure matches what the `answer` function expects as chat_history.
    """
    pairs: list[tuple[str, str]] = []
    current_pair: list[str] = []

    for turn in st.session_state.history:
        if turn["role"] == "user":
            # Start a new pair: [user_message, assistant_reply (placeholder)]
            current_pair = [turn["content"], ""]
        else:
            # Finalize the pair when we encounter the assistant side
            if current_pair:
                current_pair[1] = turn["content"]
                pairs.append(tuple(current_pair))
                current_pair = []

    return pairs[-limit:]


# ======================================================================================================
# Chat interaction
# ======================================================================================================

def handle_user_input() -> None:
    """
    Read user input, call meta-handling if necessary, or forward the query to the retrieval backend.
    The sequence of operations mirrors the original logic.
    """
    user_query = st.chat_input("Frage eingeben …")
    has_new_question = bool(user_query)

    if not (has_new_question and user_query.strip()):
        return

    # Store user message
    st.session_state.history.append({"role": "user", "content": user_query})
    st.session_state.history = st.session_state.history[-200:]  # limit history size

    # Handle meta questions separately
    if handle_meta_questions(user_query):
        return

    # Regular question answered via retrieval pipeline
    with st.spinner("Thinking …"):
        try:
            recent_turns = get_recent_chat_turn_pairs(limit=5)
            response = generate_answer(user_query, recent_turns)
        except Exception as exc:
            logger.exception("Error while generating answer.")
            response = f"Fehler: {exc}"

    # Store assistant response
    st.session_state.history.append({"role": "assistant", "content": response})
    st.session_state.history = st.session_state.history[-200:]


def render_chat_history() -> None:
    """
    Display the full chat history in a modern chat layout.
    """
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ======================================================================================================
# Main entry point
# ======================================================================================================

def main() -> None:
    """
    Main entry point for the RAG-BOT Streamlit application.
    Sets up the UI, initializes background services, and manages the chat loop.
    """
    configure_page()
    apply_global_styles()

    logo_b64 = load_logo_base64()
    render_sidebar(logo_b64)

    initialize_watchdog()
    trigger_initial_ingestion_if_needed()

    ensure_chat_history_initialized()
    handle_user_input()
    render_chat_history()


if __name__ == "__main__":
    main()

