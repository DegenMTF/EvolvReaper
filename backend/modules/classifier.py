# modules/classifier.py
from db import get_connection

KEYWORDS = {
    "finance": ["bank", "invest", "fund", "loan", "credit", "capital"],
    "health": ["clinic", "health", "med", "care"],
    "tech": ["cloud", "tech", "software", "data", "digital"],
    "legal": ["law", "legal", "attorney"],
}

def classify_all():
    print("[Classifier] Classifying domains...")

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, domain FROM domains WHERE industry='' OR industry IS NULL")
    rows = c.fetchall()

    for row in rows:
        ind = ""
        domain = row["domain"].lower()

        for industry, words in KEYWORDS.items():
            if any(w in domain for w in words):
                ind = industry
                break

        if ind:
            c.execute("UPDATE domains SET industry=? WHERE id=?", (ind, row["id"]))

    conn.commit()
    conn.close()
    print("[Classifier] Done.")