# modules/commoncrawl.py
import requests
from db import get_connection

CC_INDEXES = [
    "https://index.commoncrawl.org/CC-MAIN-2024-10-index",
    "https://index.commoncrawl.org/CC-MAIN-2023-50-index",
    "https://index.commoncrawl.org/CC-MAIN-2023-40-index"
]

def scrape():
    print("[CommonCrawl] Starting extraction...")

    conn = get_connection()
    c = conn.cursor()

    for index in CC_INDEXES:
        try:
            print(f"[CommonCrawl] Fetching index: {index}")
            r = requests.get(f"{index}?url=*.com&output=json")

            if r.status_code != 200:
                print(f"[CommonCrawl] Error fetching: {index}")
                continue

            for line in r.text.splitlines():
                try:
                    url = line.split('"url": "')[1].split('"')[0]
                    domain = url.replace("http://", "").replace("https://", "").split("/")[0]

                    c.execute("""
                        INSERT OR IGNORE INTO domains (domain, country, industry, source)
                        VALUES (?, ?, ?, ?)
                    """, (domain, "", "", "commoncrawl"))

                except:
                    pass

            conn.commit()

        except Exception as e:
            print("[CommonCrawl] ERROR:", e)

    conn.close()
    print("[CommonCrawl] Done.")