# modules/validator.py
import dns.resolver
from db import get_connection

def validate_all():
    print("[Validator] Validating domains...")

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, domain FROM domains")
    rows = c.fetchall()

    for row in rows:
        domain = row["domain"]

        try:
            dns.resolver.resolve(domain, "A")  # has IP
            dns.resolver.resolve(domain, "MX") # has mail server
        except:
            continue  # skip invalid domains

    print("[Validator] Validation completed.")
    conn.close()