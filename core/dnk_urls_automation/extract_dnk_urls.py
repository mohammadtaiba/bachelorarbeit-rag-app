import re
from pathlib import Path
from utils.logger import logger

def extract_dnk_urls(_year: int):
    logger.info("Extrahiere DNK URLs ...")

    # Input-file
    input_file = f"../../data/url_sources/dnk_{_year}_individually.txt"

    # Output-file
    output_file = Path(f"../../data/url_sources/dnk_{_year}_all.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # aller Inhalte IDs
    ranges = {
        1: range(1, 2),     # 1_1
        2: range(1, 5),     # 2_1 ... 2_4
        3: range(1, 11),    # 3_1 ... 3_10
        4: range(1, 6),     # 4_1 ... 4_5
        5: range(1, 13)     # 5_1 ... 5_12
    }

    # Liste aller erzeugten URLs
    urls = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            base_url = line.strip()
            if not base_url:
                continue # ignore empty line

            # Basis-URL ohne MainMenuHandler extrahieren
            prefix = re.sub(r"MainMenuHandler/\d+_\d+", "MainMenuHandler/{}", base_url)

            # URLs für diese Base-URL erzeugen
            for chapter, numbers in ranges.items():
                for number in numbers:
                    urls.append(prefix.format(f"{chapter}_{number}"))

    # Alle URLs in Datei schreiben
    with open(output_file, "w", encoding="utf-8") as f:
        for u in urls:
            f.write(u + "\n")

    logger.info(f"    - Anzahl erzeugter URLs: {len(urls)}")
    logger.info("Extraktion abgeschlossen.")