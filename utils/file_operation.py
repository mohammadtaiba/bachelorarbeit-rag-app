# utils/file_operations.py
from utils.logger import logger
from pathlib import Path
from core.preprocess import UPLOAD_PATH, RAW_PATH, TEMP_MD_PATH, FINAL_MD_PATH
import shutil
import pythoncom
import win32com.client as win32

# -----------------------------------------------------------------------------------------------------------------
# Hilfsfunktion: Macht aus einem normalen Pfad einen "Long Path" (\\?\), damit Word auch
# sehr lange Windows-Pfade öffnen kann (> 260 Zeichen).
def _to_longpath(p: Path) -> str:
    p = p.resolve()  # absolute Pfadangabe erzwingen
    s = str(p)
    # Wenn Pfad sehr lang ist und noch kein Präfix hat → Präfix hinzufügen
    return f"\\\\?\\{s}" if len(s) > 240 and not s.startswith("\\\\?\\") else s

# -----------------------------------------------------------------------------------------------------------------
# konvertiert doc zu docx
def convert_doc_to_docx():
    doc_files = sorted(UPLOAD_PATH.glob("*.doc"))
    if not doc_files:
        logger.info("Keine DOC-Dateien in \"upload\" zum Konvertieren gefunden.")
        return

    logger.info("Konvertiere von doc zu docx ...")
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
                logger.info(f"→ {doc.name} → {doc.with_suffix('.docx').name} konvertiert")

            except Exception as e:
                logger.exception(f"⚠️ Fehler bei der Konvertierung von doc-2-docx {doc.name}: {e}")

    finally:
        # Word-Anwendung immer beenden, egal ob Fehler oder Erfolg
        word.Quit()
    logger.info("Konvertierung von doc zu docx abgeschlossen.")

# -----------------------------------------------------------------------------------------------------------------
# löscht die doc-Dateien (nach der Bearbeitung)
def delete_doc_files():
    doc_files = list(UPLOAD_PATH.glob("*.doc"))
    if not doc_files:
        logger.info("Keine DOC-Dateien in \"upload\" zum Löschen gefunden.")
        return

    logger.info("Lösche doc-Dateien ...")
    for f in doc_files:
        try:
            f.unlink()  # Datei löschen
            logger.info(f"Gelöscht Doc-Name: {f.name}")
        except Exception as e:
            logger.exception(f"⚠️ Fehler beim Löschen von {f.name}: {e}")
    logger.info("Löschen vom doc-Dateien in \"upload\" beendet.")

# -----------------------------------------------------------------------------------------------------------------
# Verschiebt alle Dateien aus UPLOAD_PATH → RAW_PATH.
def move_upload2raw():
    files = list(UPLOAD_PATH.glob("*"))
    if not files:
        logger.info("Keine Dateien in \"upload\" gefunden.")
        return

    logger.info("Verschiebe aus \"upload\" zu \"raw\"  ...")
    for f in files:
        try:
            target = RAW_PATH / f.name   # baut einfach den Zielpfad zusammen
            shutil.move(str(f), target) # verschiebt die Datei f an den neuen Ort target
            logger.info(f"    - {f.name} → nach raw/ verschoben")
        except Exception as e:
            logger.exception(f"⚠️ Fehler beim Verschieben von {f.name}: {e}")
    logger.info("Verschiebung aus \"upload\" zu \"raw\"  abgeschlossen.")


# -----------------------------------------------------------------------------------------------------------------
# Verschiebt alle Dateien aus TEMP_MD_PATH → FINAL_MD_PATH.
def move_temp2markdown():
    files = list(TEMP_MD_PATH.glob("*.md"))
    if not files:
        logger.info("Keine Markdown-Dateien in \"markdown_temp\" gefunden.")
        return

    logger.info("Verschiebe aus \"markdown_temp\" zu \"markdown\"  ...")

    for f in files:
        try:
            target = FINAL_MD_PATH / f.name
            f.replace(target)  # schneller als shutil.move für gleiche Partition
            logger.info(f"    - {f.name} → nach markdown/ verschoben")
        except Exception as e:
            logger.exception(f"⚠️ Fehler beim Verschieben von {f.name}: {e}")
    logger.info("Verschiebung aus \"markdown_temp\" zu \"markdown\"  abgeschlossen.")