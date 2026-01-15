# utils/export_txt.py
from db import get_connection
from pathlib import Path

def generate():
    output_file = Path(__file__).parents[1] / "output" / "domains.txt"
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT domain FROM domains ORDER BY domain ASC")
    domains = c.fetchall()

    with open(output_file, "w") as f:
        for d in domains:
            f.write(d["domain"] + "\n")

    return output_file