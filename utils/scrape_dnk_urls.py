import requests
import time
import concurrent.futures
from pathlib import Path

from utils.logger import logger

# DNK-URL
BASE_URL = ("https://datenbank2.deutscher-nachhaltigkeitskodex.de/"
            "Profile/MainMenuHandler/2_1?company={company}&year=2024&lang=de&culture=de")

# Speicherort festlegen
OUTPUT_FILE = Path("../data/url_sources/dnk_2024.txt")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# ======================================================================================================
# Helferfunktion: URLs überprüfen
# ======================================================================================================
def check_company(session: requests.Session, company_id: int) -> tuple[int, bool]:
    url = BASE_URL.format(company=company_id)
    try:
        resp = session.get(url, timeout=5)
    except requests.RequestException:
        return company_id, False

    if resp.status_code != 200:
        return company_id, False

    if len(resp.text) < 1000:
        return company_id, False

    return company_id, True

# ======================================================================================================
# Hauptfunktion: URLs überprüfen und in `dnk_2024.txt` sammeln
# ======================================================================================================
def scrape_dnk_urls():
    start_id    = 12000
    end_id      = 19000
    max_workers = 20

    logger.info(f"Starting DNK scraping from ID {start_id} to {end_id}...")

    t0 = time.perf_counter()

    with requests.Session() as session:
        session.headers.update({"User-Agent": "DNK-Scraper/1.0 (kontakt@example.com)"})

        with OUTPUT_FILE.open("w", encoding="utf-8") as f_out:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(check_company, session, cid)
                    for cid in range(start_id, end_id)
                ]

                checked = 0
                valid   = 0

                for future in concurrent.futures.as_completed(futures):
                    company_id, exists = future.result()
                    checked += 1

                    if exists:
                        valid += 1
                        url = (f"https://datenbank2.deutscher-nachhaltigkeitskodex.de/"
                               f"Profile/MainMenuHandler/1_1?company={company_id}"
                               f"&year=2024&lang=de&culture=de")
                        f_out.write(url + "\n")

    elapsed = time.perf_counter() - t0
    logger.info(f"{checked} URLs geprüft, {valid} gültige URLs gefunden in {elapsed:.2f}s")



if __name__ == "__main__":
    scrape_dnk_urls()
