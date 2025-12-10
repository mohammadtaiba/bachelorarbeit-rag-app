import requests
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as mdify
from utils.logger import logger

OUTPUT_DIR = Path("../../data/upload")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def dnk_urls_2_md(_year: int):
    logger.info("HTML laden und in Markdown konvertieren …")

    URL_FILE = Path(f"../../data/url_sources/dnk_{_year}_individually.txt")

    # URLs aus Datei-(URL_FILE) lesen
    urls = [u.strip() for u in URL_FILE.read_text(encoding="utf-8").splitlines() if u.strip()]


    # jede 32 URLs → 1 Datei
    GROUP_SIZE = 32
    groups = [urls[i:i + GROUP_SIZE] for i in range(0, len(urls), GROUP_SIZE)]

    for file_index, group in enumerate(groups, start=1):

        output_file = OUTPUT_DIR / f"dnk_datei_{_year}_{file_index}.md"
        output_file.write_text("", encoding="utf-8")

        for url in group:

            try:
                # HTML abrufen
                r = requests.get(url, headers={"User-Agent": "MD-Scraper"})
                if "html" not in r.headers.get("Content-Type", "").lower():
                    logger.warning(f"⚠️ Übersprungen (kein HTML): {url}")
                    continue

                # HTML parsen
                soup = BeautifulSoup(r.text, "html.parser")

                # HTML bereinigen
                for tag in soup.find_all("a"): tag.unwrap()      # Links entfernen: <a> bleibt Text
                for tag in soup.find_all("img"): tag.decompose() # Bilder entfernen: komplette <img>-Tags löschen

                # Bereinigtes HTML → Markdown, dann speichern
                markdown = mdify(str(soup), heading_style="ATX")

                output_file.write_text(
                    output_file.read_text(encoding="utf-8") +
                    f"\n\n" + markdown,encoding="utf-8"
                )
                logger.debug(f"    - Gespeichert: {url}")

            except Exception:
                logger.exception("⚠️ Fehler beim Verarbeiten der URL")

    logger.info("HTML laden und in Markdown konvertierung ist abgeschlossen.")