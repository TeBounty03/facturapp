# services/invoice_service.py
import sqlite3
from datetime import datetime
from facturapp.utils.database import DB_PATH, generate_invoice_number

def save_invoice(customer_id, items, flid=None, status="Draft"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    invoice_date = datetime.now().strftime("%Y-%m-%d")
    number = generate_invoice_number()
    total_amount = sum(qty * price for (_, _, _, qty, price, _) in items)

    # ➤ Insertion de l'en-tête (avec ou sans FLID)
    if flid:
        cursor.execute(
            "INSERT INTO invoices (customer_id, number, date, flid, status, total) VALUES (?, ?, ?, ?, ?, ?)",
            (customer_id, number, invoice_date, flid, status, total_amount)
        )
    else:
        cursor.execute(
            "INSERT INTO invoices (customer_id, number, date, status, total) VALUES (?, ?, ?, ?, ?)",
            (customer_id, number, invoice_date, status, total_amount)
        )

    invoice_id = cursor.lastrowid

    # ➤ Insertion des lignes
    for item in items:
        # item = (project, flid_line, description, qty, price, total)
        project_id, _, description, quantity, unit_price, total = item
        cursor.execute(
            "INSERT INTO items (invoice_id, project_id, description, quantity, unit_price, total) VALUES (?, ?, ?, ?, ?, ?)",
            (invoice_id, project_id, description, quantity, unit_price, total)
        )

    conn.commit()
    conn.close()
    return number
