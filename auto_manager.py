import os
from shutil import rmtree
import shutil
from core.preprocess import DB_PATH, RAW_PATH, UPLOAD_PATH, FINAL_MD_PATH

"""
 löscht direkt: db/ und data/markdown
"""
def auto_delete_db_markdown():
    # --- db/chroma löschen ---
    if DB_PATH.exists():
        rmtree(DB_PATH)
        print("DB-Daten wurden gelöscht.")
    else:
        print("Es existiert keine DB-Daten!")

    # --- data/markdown/* löschen ---
    if FINAL_MD_PATH.exists() and any(FINAL_MD_PATH.glob("*")):
        for file in FINAL_MD_PATH.glob("*"):
            file.unlink()
        print("Markdown-Ordner wurden geleert.")
    else:
        print("Markdown-Ordner ist leer!")

"""
 Auswahl: löschen oder (schieben data/raw nach data/upload)
"""
def auto_raw():
    # --- data/raw/* löschen/ verschieben? ---
    if RAW_PATH.exists() and any(RAW_PATH.glob("*")):
        input_raw = input(" 0) Löschen \n 1) Behalten \n 2) nach upload verschieben \n → Gebe eine Zahl ein: ").strip()
        if input_raw== "0":
            for file in RAW_PATH.glob("*"):
                file.unlink()
            print("Raw-Ordner wurden geleert.")

        elif input_raw == "1":
            print("Raw-Dateien wurden behalten")

        elif input_raw == "2":
            for file in RAW_PATH.glob("*"):
                shutil.move(str(file), UPLOAD_PATH / file.name)
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
        2) Raw-Dateien löschen oder verschieben
        3) Indizieren
        4) ChatBot starten
        5) Beenden""")

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
                print("Beendet.")
                break
            else:
                print("Ungültige Eingabe, bitte erneut versuchen:")


if __name__ == "__main__":
    auto_manager()