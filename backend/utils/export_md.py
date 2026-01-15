# utils/export_md.py
from db import get_connection
from pathlib import Path

def generate():
    output_file = Path(__file__).parents[1] / "output" / "domains.md"
    conn = get_connection()
    c = conn.cursor()

    with open(output_file, "w") as f:
        f.write("# Domain Harvester Results\n\n")

        c.execute("SELECT DISTINCT industry FROM domains")
        industries = c.fetchall()

        for ind in industries:
            name = ind["industry"] or "uncategorized"
            f.write(f"## {name.title()}\n")

            c.execute("SELECT domain FROM domains WHERE industry=?", (name,))
            domains = c.fetchall()

            for d in domains:
                f.write(f"- {d['domain']}\n")

            f.write("\n")

    return output_file