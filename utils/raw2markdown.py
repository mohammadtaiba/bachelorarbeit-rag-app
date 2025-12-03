# utils/raw2markdown.py
import pandas as pd
import pymupdf4llm as pml
from streamlit import header
from core.preprocess import UPLOAD_PATH, TEMP_MD_PATH
import pypandoc
from utils.logger import logger

# ---------------------------------------------------------------------------------------------------------------------
def convert_all_to_markdown():

    # -----------------------------------------------------------------------------------------------------------------
    # ---- pdf2md ----
    logger.info("Starte Konvertierung der Rohdaten zu Markdown ...")

    pdf_files = sorted(UPLOAD_PATH.glob("*.pdf"))
    if not pdf_files:
        logger.info(f"Keine PDFs in {UPLOAD_PATH.resolve()} gefunden.")
    else:
        for pdf in pdf_files:
            try:
                md = pml.to_markdown(str(pdf), write_images=False)
                (TEMP_MD_PATH / (pdf.stem + ".md")).write_text(md, encoding="utf-8")
                logger.info("    - konvertiert:", pdf.name)
            except Exception as e:
                logger.exception("⚠️ Fehler bei der Konvertierung der PDF-Datei.")

        logger.info(f"Anzahl der konvertierten PDFs {len(pdf_files)}.")

    # -----------------------------------------------------------------------------------------------------------------
    # ---- docx2gfm ----
    docx_files = sorted(UPLOAD_PATH.glob("*.docx"))
    if not docx_files:
        logger.info(f"Keine DOCX in {UPLOAD_PATH.resolve()} gefunden.")
    else:
        for docx in docx_files:
            try:
                md = pypandoc.convert_file(
                    str(docx),
                    to="markdown+pipe_tables",
                    format="docx",
                    extra_args=[
                        "--wrap=none",
                        "--markdown-headings=atx",
                        "--reference-links"
                    ],
                )
                (TEMP_MD_PATH / (docx.stem + ".md")).write_text(md, encoding="utf-8")
                logger.info("    - konvertiert:", docx.name)
            except Exception as e:
                logger.exception("⚠️ Fehler bei der Konvertierung der Word-Datei.")
        logger.info(f"Anzahl der konvertierten DOCX {len(docx_files)}.")

    # -----------------------------------------------------------------------------------------------------------------
    # ---- xlsx2md ----
    xlsx_files = sorted(UPLOAD_PATH.glob("*.xlsx")) + sorted(UPLOAD_PATH.glob("*.xls"))
    if not xlsx_files:
        logger.info(f"Keine Excel-Dateien in {UPLOAD_PATH.resolve()} gefunden.")
    else:
        # openpyxl-Header/Footer-Warnung einmalig ausblenden
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

        for xlsx in xlsx_files:
            try:
                # Context Manager sorgt dafür, dass die Datei-Handles IMMER geschlossen werden
                with pd.ExcelFile(xlsx, engine="openpyxl") as excel:
                    md_parts = []

                    for sheet_name in excel.sheet_names:
                        df = excel.parse(sheet_name)

                        # optional: NaN -> leer, damit Markdown „schöner“ ist
                        df = df.fillna("")

                        if df.empty:
                            logger.info(f"    (übersprungen - leeres Sheet): {xlsx.name} → {sheet_name}")
                            continue

                        sheet_md = df.to_markdown(index=False, tablefmt="pipe")
                        md_parts.append(f"## {sheet_name}\n\n{sheet_md}\n")

                if not md_parts:
                    logger.info(f"    (keine verwertbaren Sheets): {xlsx.name}")
                    continue

                # Zusammenführen zu einer Datei pro Excel
                (TEMP_MD_PATH / f"{xlsx.stem}.md").write_text("\n\n".join(md_parts), encoding="utf-8")
                logger.info(f"    - konvertiert: {xlsx.name}")

            except Exception as e:
                logger.exception("⚠️ Fehler bei der Konvertierung der Excel-Datei.")

        logger.info(f"Anzahl der konvertierten Excel-Dateien {len(xlsx_files)}.")

    # -----------------------------------------------------------------------------------------------------------------
    logger.info("Konvertierung abgeschlossen.")