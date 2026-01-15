# utils/export_json.py
from db import get_connection
from pathlib import Path
import json

def generate():
    output_file = Path(__file__).parents[1] / "output" / "domains.json"
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT domain, country, industry, source FROM domains ORDER BY domain ASC")
    rows = [dict(r) for r in c.fetchall()]

    with open(output_file, "w") as f:
        json.dump(rows, f, indent=4)

    return output_file