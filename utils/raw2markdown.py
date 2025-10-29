# utils/raw2markdown.py
import pymupdf4llm as pml
from core.config import UPLOAD_DIR, MARKDOWN_TEMP_DIR
import pypandoc

def convert_all_to_markdown():
    # ---- pdf2md ----
    print("Starte Konvertierung der Rohdaten zu Markdown ...")

    pdf_files = sorted(UPLOAD_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"Keine PDFs in {UPLOAD_DIR.resolve()} gefunden.")
    else:
        for pdf in pdf_files:
            md = pml.to_markdown(str(pdf), write_images=False)
            (MARKDOWN_TEMP_DIR / (pdf.stem + ".md")).write_text(md, encoding="utf-8")
            print("    - konvertiert:", pdf.name)
        print(f"Anzahl der konvertierten PDFs {len(pdf_files)}.")

    # ---- docx2gfm ----
    docx_files = sorted(UPLOAD_DIR.glob("*.docx"))
    if not docx_files:
        print(f"Keine DOCX in {UPLOAD_DIR.resolve()} gefunden.")
    else:
        for docx in docx_files:
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
            (MARKDOWN_TEMP_DIR / (docx.stem + ".md")).write_text(md, encoding="utf-8")
            print("    - konvertiert:", docx.name)
        print(f"Anzahl der konvertierten DOCX {len(docx_files)}.")

    print("Konvertierung abgeschlossen.")