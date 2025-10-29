# utils/cleanup_md.py
import re
from core.config import MARKDOWN_TEMP_DIR

# --- Regex-Definitionen ---
# HTML-Elemente entfernen
FIGURE_RE = re.compile(r"<figure[\s\S]*?</figure>", re.IGNORECASE)
IMG_RE = re.compile(r"<img[^>]*>", re.IGNORECASE)
FIGCAP_RE = re.compile(r"<figcaption[\s\S]*?</figcaption>", re.IGNORECASE)
EMPTY_TD_RE = re.compile(r"\s*<td>\s*</td>\s*", re.IGNORECASE)

# Zeilen mit nur "\-" (auch mit Leerzeichen drumherum) löschen
ESCAPED_DASH_LINE_RE = re.compile(r"^\s*\\-\s*$", re.MULTILINE)

# Tabellenreste entfernen
EMPTY_TABLE_LINE_RE = re.compile(r"\n?\|\s*(\|\s*)+\|?\n?", re.MULTILINE)
SINGLE_PIPE_RE = re.compile(r"\n?\s*\|\s*\n?", re.MULTILINE)

DASH_LINE_RE = re.compile(r"-{4,}")  # lange Strichfolgen reduzieren → ---
EQUAL_LINE_RE = re.compile(r"={4,}")  # viele "=" -> ===
TOC_TAG_RE = re.compile(r"#?_Toc\d+", re.IGNORECASE) # Anker für Tabellen
REFERENCE_LINE_RE = re.compile(r"^\s*\[\d+\]:\s*$", re.MULTILINE) # Pandoc-Referenzlinks

def cleanup_md():
    print("Bereinige der Markdown-Dateien ...")
    for ext in ("*.md", "*.gfm"):
        for md_file in MARKDOWN_TEMP_DIR.glob(ext):
            text = md_file.read_text(encoding="utf-8")

            # HTML-Elemente entfernen
            text = FIGURE_RE.sub("", text)
            text = IMG_RE.sub("", text)
            text = FIGCAP_RE.sub("", text)
            text = EMPTY_TD_RE.sub("", text)
            text = ESCAPED_DASH_LINE_RE.sub("", text)
            text = EMPTY_TABLE_LINE_RE.sub("", text)
            text = SINGLE_PIPE_RE.sub("", text)
            text = DASH_LINE_RE.sub("---", text)
            text = EQUAL_LINE_RE.sub("===", text)
            text = TOC_TAG_RE.sub("", text)
            text = REFERENCE_LINE_RE.sub("", text)

            # Überflüssige Leerzeichen am Anfang/Ende
            text = text.strip()

            # Mehrfache Leerzeichen → ein Leerzeichen
            text = re.sub(r"[ \t]+", " ", text)

            # entfernt alle komplett leeren Zeilen (auch wenn sie nur aus Leerzeichen bestehen)
            text = re.sub(r"^\s*\n", "", text, flags=re.MULTILINE)

            md_file.write_text(text, encoding="utf-8")
            print(f"   - Bereinigt → {md_file.name}")

    print("Bereinigung abgeschlossen.")

if __name__ == "__main__":
    cleanup_md()
