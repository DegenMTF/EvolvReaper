# modules/certscan.py
import requests
from db import get_connection

CRT_API = "https://crt.sh/?q=%.finance&output=json"

def scrape():
    print("[CertScan] Starting certificate scraping...")

    conn = get_connection()
    c = conn.cursor()

    try:
        r = requests.get(CRT_API)
        if r.status_code != 200:
            print("[CertScan] API error")
            return

        certs = r.json()

        for cert in certs:
            domain = cert.get("common_name")
            if domain and "*" not in domain:
                domain = domain.strip()

                c.execute("""
                    INSERT OR IGNORE INTO domains (domain, country, industry, source)
                    VALUES (?, ?, ?, ?)
                """, (domain, "", "finance", "certscan"))

        conn.commit()

    except Exception as e:
        print("[CertScan] ERROR:", e)

    conn.close()
    print("[CertScan] Done.")