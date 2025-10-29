# utils/file_operations.py
from pathlib import Path
from core.config import UPLOAD_DIR, RAW_DIR, MARKDOWN_DIR, MARKDOWN_TEMP_DIR
import shutil

# --- Hilfsfunktion ---
# Macht aus einem normalen Pfad einen "Long Path" (\\?\), damit Word auch
# sehr lange Windows-Pfade öffnen kann (> 260 Zeichen).
def _to_longpath(p: Path) -> str:
    p = p.resolve()  # absolute Pfadangabe erzwingen
    s = str(p)
    # Wenn Pfad sehr lang ist und noch kein Präfix hat → Präfix hinzufügen
    return f"\\\\?\\{s}" if len(s) > 240 and not s.startswith("\\\\?\\") else s


def convert_doc_to_docx():
    print("Konvertiere von doc zu docx ...")

    import pythoncom
    import win32com.client as win32

    doc_files = sorted(UPLOAD_DIR.glob("*.doc"))
    print("Gefundene DOC-Dateien:", [f.name for f in doc_files])

    if not doc_files:
        print("Keine DOC-Dateien zum Konvertieren gefunden.")
        return

    # COM-Initialisierung (notwendig für win32)
    pythoncom.CoInitialize()

    # Word-Instanz starten (unsichtbar)
    word = win32.Dispatch("Word.Application")
    word.Visible = False

    try:
        for doc in doc_files:
            # Quell- und Zielpfad vorbereiten
            src = _to_longpath(doc)
            dst = _to_longpath(doc.with_suffix(".docx"))

            try:
                # Datei mit Word öffnen (kein Dialog, kein ReadOnly)
                wdoc = word.Documents.Open(
                    src,
                    ConfirmConversions=False,
                    ReadOnly=False,
                    AddToRecentFiles=False
                )

                # Als DOCX speichern (FileFormat=16 "neues XML-basiertes Format")
                wdoc.SaveAs2(dst, FileFormat=16)
                wdoc.Close(False)
                print(f"→ {doc.name} → {doc.with_suffix('.docx').name} konvertiert")

            except Exception as e:
                print(f"⚠️ Fehler bei {doc.name}: {e}")

    finally:
        # Word-Anwendung immer beenden, egal ob Fehler oder Erfolg
        word.Quit()
    print("Konvertierung abgeschlossen.")


def delete_doc_files():
    print("Lösche doc-Dateien ...")
    doc_files = list(UPLOAD_DIR.glob("*.doc"))

    if not doc_files:
        print("Keine DOC-Dateien zum Löschen gefunden.")
        return

    for f in doc_files:
        try:
            f.unlink()  # Datei löschen
            print(f"Gelöscht Doc-Name: {f.name}")
        except Exception as e:
            print(f"⚠️ Fehler beim Löschen von {f.name}: {e}")
    print("Lösche beendet.")


# Verschiebt alle Dateien aus UPLOAD_DIR → RAW_DIR.
def move_upload2raw():
    print("Verschiebe aus UPLOAD_DIR → RAW_DIR ...")
    files = list(UPLOAD_DIR.glob("*"))

    if not files:
        print("Keine Dateien in upload/ gefunden.")
        return

    for f in files:
        try:
            target = RAW_DIR / f.name   # baut einfach den Zielpfad zusammen
            shutil.move(str(f), target) # verschiebt die Datei f an den neuen Ort target
            print(f"    - {f.name} → nach raw/ verschoben")
        except Exception as e:
            print(f"⚠️ Fehler beim Verschieben von {f.name}: {e}")
    print("Verschiebung abgeschlossen.")


# Verschiebt alle Dateien aus MARKDOWN_TEMP_DIR → MARKDOWN_DIR.
def move_temp2markdown():
    print("Verschiebe aus MARKDOWN_TEMP_DIR → MARKDOWN_DIR ...")
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
    files = list(MARKDOWN_TEMP_DIR.glob("*.md"))

    if not files:
        print("Keine Markdown-Dateien in markdown_temp/ gefunden.")
        return

    for f in files:
        try:
            target = MARKDOWN_DIR / f.name
            f.replace(target)  # schneller als shutil.move für gleiche Partition
            print(f"    - {f.name} → nach markdown/ verschoben")
        except Exception as e:
            print(f"⚠️ Fehler beim Verschieben von {f.name}: {e}")
    print("Verschiebung abgeschlossen.")