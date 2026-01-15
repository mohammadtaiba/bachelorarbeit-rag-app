# utils/manage_files.py
import pandas as pd
import shutil
from markitdown import MarkItDown

from utils.logger import logger
from core.config import PATH_PROCESSING, PATH_PROCESSED, PATH_UPLOAD, PATH_RAW

# ======================================================================================================
# Konvertiere alle Dateien in der UPLOAD zu MD-Dateien
# ======================================================================================================
def convert_all_to_markdown():
    logger.info(f"Starte Konvertierung der Rohdaten aus dem Ordner ({PATH_UPLOAD.resolve()}) zu Markdown ...")

    # -----------------------------------------------------------------------------------------------------------------
    # pdf2md
    # -----------------------------------------------------------------------------------------------------------------
    md_converter = MarkItDown()
    pdf_files    = sorted(PATH_UPLOAD.glob("*.pdf"))

    if not pdf_files:
        logger.info(f"    - Es existiert keine PDFs.")
    else:
        for pdf in pdf_files:
            try:
                result = md_converter.convert(str(pdf))
                md_text = result.text_content

                (PATH_PROCESSING / (pdf.stem + ".md")).write_text(md_text, encoding="utf-8")
                logger.debug(f"    - konvertiert: {pdf.name}")

            except Exception as e:
                logger.exception(f"⚠️ Fehler bei der Konvertierung der PDF-Datei {pdf.name}")

        logger.info(f"    - Anzahl der konvertierten PDFs: {len(pdf_files)}.")

    # -----------------------------------------------------------------------------------------------------------------
    # docx2gfm
    # -----------------------------------------------------------------------------------------------------------------
    docx_files = sorted(PATH_UPLOAD.glob("*.docx"))
    if not docx_files:
        logger.info(f"    - Es existiert keine DOCX.")
    else:
        md_converter = MarkItDown()

        for docx in docx_files:
            try:
                result = md_converter.convert(str(docx))
                md_text = result.text_content

                (PATH_PROCESSING / (docx.stem + ".md")).write_text(md_text, encoding="utf-8")
                logger.debug(f"    - konvertiert: {docx.name}")

            except Exception as e:
                logger.exception(f"⚠️ Fehler bei der Konvertierung der Word-Datei {docx.name}")

        logger.info(f"    - Anzahl der konvertierten DOCX: {len(docx_files)}.")

    # -----------------------------------------------------------------------------------------------------------------
    # xlsx2md (optimiert)
    # -----------------------------------------------------------------------------------------------------------------
    xlsx_files = sorted(PATH_UPLOAD.glob("*.xlsx")) + sorted(PATH_UPLOAD.glob("*.xls"))
    if not xlsx_files:
        logger.info(f"    - Es existiert keine XLSXs.")
    else:
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

        for xlsx in xlsx_files:
            try:
                md_parts = []

                with pd.ExcelFile(xlsx, engine="openpyxl") as excel:
                    for sheet in excel.sheet_names:
                        df = excel.parse(sheet).fillna("")

                        if df.empty:
                            logger.info(f"    (übersprungen - leeres Sheet): {xlsx.name} → {sheet}")
                            continue

                        md_parts.append(
                            f"## {sheet}\n\n{df.to_markdown(index=False, tablefmt='pipe')}\n"
                        )

                if not md_parts:
                    logger.info(f"    (keine verwertbaren Sheets): {xlsx.name}")
                    continue

                (PATH_PROCESSING / f"{xlsx.stem}.md").write_text("\n\n".join(md_parts), encoding="utf-8")
                logger.debug(f"    - konvertiert: {xlsx.name}")

            except Exception as e:
                logger.exception(f"⚠️ Fehler bei der Konvertierung der Excel-Datei {xlsx.name}")

        logger.info(f"    - Anzahl der konvertierten Excel-Dateien: {len(xlsx_files)}.")


    # -----------------------------------------------------------------------------------------------------------------
    # txt-dateien umbenennen und nach processing verschieben
    # -----------------------------------------------------------------------------------------------------------------
    txt_files = sorted(PATH_UPLOAD.glob("*.txt"))
    if not txt_files:
        logger.info(f"    - Es existiert keine TXTs.")
    else:
        for txt in txt_files:
            target = PATH_PROCESSING / f"{txt.stem}.md" # umbenennen
            txt.rename(target) # verschieben
            logger.debug(f"    - konvertiert: {txt.name}")
        logger.info(f"    - Anzahl der konvertierten TXT-Dateien: {len(txt_files)}.")

    # -----------------------------------------------------------------------------------------------------------------
    # markdown-dateien automatisch nach processing verschieben
    # -----------------------------------------------------------------------------------------------------------------
    md_files = sorted(PATH_UPLOAD.glob("*.md"))
    if not md_files:
        logger.info(f"    - Es existiert keine MDs.")
    else:
        for md in md_files:
            target = PATH_PROCESSING / md.name
            md.rename(target) # Datei verschieben
            logger.debug(f"    - konvertiert: {md.name}")
        logger.info(f"    - Anzahl der konvertierten MD-Dateien: {len(md_files)}.")

    # -----------------------------------------------------------------------------------------------------------------
    logger.info("Konvertierung abgeschlossen.")


# ======================================================================================================
# Verschiebt von DATA_PROCESSING → DATA_PROCESSED.
# ======================================================================================================
def move_processing2processed():
    files = list(PATH_PROCESSING.glob("*.md"))
    if not files:
        logger.info(f"Keine Markdown-Dateien in {PATH_PROCESSING.resolve()} gefunden.")
        return

    logger.info(f"Verschiebe aus {PATH_PROCESSING.resolve()} → {PATH_PROCESSED.resolve()}  ...")

    for file in files:
        try:
            target = PATH_PROCESSED / file.name
            file.replace(target)  # schneller als shutil.move für gleiche Partition
            logger.debug(f"    - {file.name} → nach {PATH_PROCESSED.resolve()} verschoben")
        except Exception as e:
            logger.exception("⚠️ Fehler beim Verschieben vom TEMP_MD_Ordner zu FINAL_MD_Ordner.")
    logger.info(f"Verschiebung abgeschlossen.")


# ======================================================================================================
# Verschiebt alle Dateien aus UPLOAD-Ordner → RAW-Ordner.
# ======================================================================================================
def move_upload2raw():
    files = list(PATH_UPLOAD.glob("*"))
    if not files:
        logger.info(f"Keine Dateien in {PATH_UPLOAD.resolve()} gefunden.")
        return

    logger.info(f"Verschiebe aus {PATH_UPLOAD.resolve()} zu {PATH_RAW.resolve()} ...")
    for file in files:
        try:
            target = PATH_RAW / file.name   # baut einfach den Zielpfad zusammen
            shutil.move(str(file), target)  # verschiebt die Datei file an den neuen Ort target
            logger.debug(f"    - {file.name}")
        except Exception as e:
            logger.exception(f"⚠️ Fehler beim Verschieben von {file.name}: {e} ")
    logger.info(f"Verschiebung abgeschlossen.")