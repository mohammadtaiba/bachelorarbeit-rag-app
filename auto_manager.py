import os
from pathlib import Path
from shutil import rmtree
import shutil

db_path = Path("db/chromadb")
md_path = Path("temp/markdown")
raw_path = Path("temp/raw")
upload_path = Path("temp/upload")

"""
 löscht direkt: db/ und data/markdown
"""
def auto_delete_db_markdown():
    # --- db/chroma löschen ---
    if db_path.exists():
        rmtree(db_path)
        print("DB-Daten wurden gelöscht.")
    else:
        print("Es existiert keine DB-Daten!")

    # --- data/markdown/* löschen ---
    if md_path.exists() and any(md_path.glob("*")):
        for file in md_path.glob("*"):
            file.unlink()
        print("Markdown-Ordner wurden geleert.")
    else:
        print("Markdown-Ordner ist leer!")

"""
 Auswahl: löschen oder (schieben data/raw nach data/upload)
"""
def auto_raw():
    # --- data/raw/* löschen/ verschieben? ---
    if raw_path.exists() and any(raw_path.glob("*")):
        input_raw = input(" 0) Löschen \n 1) Behalten \n 2) nach upload verschieben \n → Gebe eine Zahl ein: ").strip()
        if input_raw== "0":
            for file in raw_path.glob("*"):
                file.unlink()
            print("Raw-Ordner wurden geleert.")

        elif input_raw == "1":
            print("Raw-Dateien wurden behalten")

        elif input_raw == "2":
            for file in raw_path.glob("*"):
                shutil.move(str(file), upload_path / file.name)
            print("Dateien wurden nach 'upload/' verschoben.")
    else:
        print("raw-Ordner ist leer!")


"""
 Auto-Manager:
"""
def auto_manager():
    while True:
            print(
    """Was möchtest du tun?
        1) Datenbank & Markdown-Ordner löschen
        2) Raw-Dateien bearbeiten
        3) Ingestion starten
        4) ChatBot starten
        5) Beenden""")

            choice = input("→ Gib eine Zahl ein: ").strip()

            if choice == "1":
                auto_delete_db_markdown()
            elif choice == "2":
                auto_raw()
            elif choice == "3":
                os.system("python -m core.ingestion")
            elif choice == "4":
                os.system("streamlit run main.py")
            elif choice == "5":
                print("Beendet.")
                break
            else:
                print("Ungültige Eingabe, bitte erneut versuchen:")


if __name__ == "__main__":
    auto_manager()