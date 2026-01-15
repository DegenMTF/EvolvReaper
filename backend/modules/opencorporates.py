# modules/opencorporates.py
import requests
from db import get_connection

API = "https://api.opencorporates.com/v0.4/companies/search?q=finance"

def scrape():
    print("[OpenCorporates] Starting extraction...")

    conn = get_connection()
    c = conn.cursor()

    try:
        r = requests.get(API)
        if r.status_code != 200:
            print("[OpenCorporates] API Error")
            return

        data = r.json()
        results = data.get("results", {}).get("companies", [])

        for company in results:
            cmp = company.get("company", {})
            domain = cmp.get("website")
            country = cmp.get("jurisdiction_code")

            if domain:
                domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")

                c.execute("""
                    INSERT OR IGNORE INTO domains (domain, country, industry, source)
                    VALUES (?, ?, ?, ?)
                """, (domain, country, "finance", "opencorporates"))

        conn.commit()

    except Exception as e:
        print("[OpenCorporates] ERROR:", e)

    conn.close()
    print("[OpenCorporates] Done.")