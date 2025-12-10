import os
from shutil import rmtree
import shutil
from core.preprocess import PATH_DB, PATH_RAW, PATH_UPLOAD, PATH_PROCESSED

"""
 löscht db/ & data/Processed
"""
def auto_delete_db_markdown():

    # ------------------------- db/chroma löschen -------------------------
    if PATH_DB.exists():
        rmtree(PATH_DB)
        print("ChromaDB wurden geleert.")
    else:
        print("ChromaDB ist schon leer!")

    # ------------------------- data/markdown/* löschen -------------------------
    if PATH_PROCESSED.exists() and any(PATH_PROCESSED.glob("*")):
        for file in PATH_PROCESSED.glob("*"):
            file.unlink()
        print("Processed-Ordner wurden geleert.")
    else:
        print("Processed-Ordner ist schon leer!")

"""
 löscht data/upload
"""
def auto_delete_upload():
    if PATH_UPLOAD.exists() and any(PATH_UPLOAD.glob("*")):
        for file in PATH_UPLOAD.glob("*"):
            file.unlink()
        print("Upload-Ordner wurden geleert.")
    else:
        print("Upload-Ordner ist schon leer!")


"""
 Auswahl: löschen oder (schieben data/raw nach data/upload)
"""
def auto_raw():
    # --- data/raw/* löschen/ verschieben? ---
    if PATH_RAW.exists() and any(PATH_RAW.glob("*")):
        input_raw = input(" 1) Löschen \n 2) Behalten \n 3) nach upload verschieben \n → Gebe eine Zahl ein: ").strip()
        if input_raw== "1":
            for file in PATH_RAW.glob("*"):
                file.unlink()
            print("Raw-Ordner wurden geleert.")

        elif input_raw == "2":
            print("Raw-Dateien wurden behalten")

        elif input_raw == "3":
            for file in PATH_RAW.glob("*"):
                shutil.move(str(file), PATH_UPLOAD / file.name)
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

        1) ChromaDB & Processed-Ordner leeren
        2) Raw-Dateien löschen oder verschieben
        3) Ingestion starten
        4) Chatbot starten
        5) Upload-Dateien löschen
        6) Beenden

    """)

            choice = input("→ Gib eine Zahl ein: ").strip()

            if choice == "1":
                print("⚠️ Bitte bestätige das Löschen mit 1: ")
                ja = input()
                if ja == "1":
                    auto_delete_db_markdown()
                else:
                    print("Ungültige Eingabe, bitte erneut versuchen:")
            elif choice == "2":
                auto_raw()
            elif choice == "3":
                os.system("python -m core.ingestion")
            elif choice == "4":
                os.system("streamlit run main.py")
            elif choice == "5":
                auto_delete_upload()
            elif choice == "6":
                print("Beendet.")
                break
            else:
                print("Ungültige Eingabe, bitte erneut versuchen:")


if __name__ == "__main__":
    auto_manager()