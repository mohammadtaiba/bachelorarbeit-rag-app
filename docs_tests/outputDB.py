from langchain_chroma import Chroma
import sys
from pathlib import Path

# Log-Verzeichnis sicherstellen
Path("logs").mkdir(exist_ok=True)

# Logdatei-Pfad
log_path = Path("logs/chroma_output.md")

with open(log_path, "w", encoding="utf-8") as f:
    sys.stdout = f  # Alles print() geht in Datei

    db = Chroma(
        collection_name="lusd_bot",
        persist_directory="db/chromadb"
    )

    print("ChromaDB Übersicht\n")
    print(f"- **Gesamtzahl:** {db._collection.count()}\n Chunks-Emebbings")

    res = db._collection.get(include=["documents", "metadatas"])

    for i, d in enumerate(res.get("documents", [])):
        print(f"> Chunk {i+1}: \n")
        print(d)
        print("\n")

# sys.stdout zurücksetzen
print(f"✅ Ausgabe gespeichert unter: {log_path.resolve()}")
