import requests
import time
import concurrent.futures
from pathlib import Path
from utils.logger import logger

BASE_URL = ("https://datenbank2.deutscher-nachhaltigkeitskodex.de/"
            "Profile/MainMenuHandler/2_1?company={company}&year={year}&lang=de&culture=de")

# ======================================================================================================
# Helferfunktion: URLs überprüfen
# ======================================================================================================
def check_company(session: requests.Session, company_id: int, year: int) -> tuple[int, bool]:
    url = BASE_URL.format(company=company_id, year=year)
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
# Hauptfunktion: URLs prüfen
# ======================================================================================================
def scrape_dnk_urls(_start_id: int, _end_id: int, year: int):
    logger.info(f"Scrape DNK URLs für Jahr {year} ...")

    OUTPUT_FILE = Path(f"../../data/url_sources/dnk_{year}_individually.txt")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    max_workers = 20
    t0 = time.perf_counter()

    with requests.Session() as session:
        session.headers.update({"User-Agent": "DNK-Scraper/1.0 (kontakt@example.com)"})

        with OUTPUT_FILE.open("w", encoding="utf-8") as f_out:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(check_company, session, cid, year)
                    for cid in range(_start_id, _end_id)
                ]

                checked = 0
                valid = 0

                for future in concurrent.futures.as_completed(futures):
                    company_id, exists = future.result()
                    checked += 1

                    if exists:
                        valid += 1
                        url = BASE_URL.format(company=company_id, year=year)
                        f_out.write(url + "\n")

    elapsed = time.perf_counter() - t0
    logger.info(f"    - {checked} URLs geprüft, {valid} gültige URLs gefunden in {elapsed:.2f}s")
    logger.info("Scraping abgeschlossen.")