# utils/export_csv.py
from db import get_connection
from pathlib import Path
import csv

def generate():
    output_file = Path(__file__).parents[1] / "output" / "domains.csv"
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT domain, country, industry, source FROM domains ORDER BY domain ASC")
    rows = c.fetchall()

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "country", "industry", "source"])

        for r in rows:
            writer.writerow([r["domain"], r["country"], r["industry"], r["source"]])

    return output_file