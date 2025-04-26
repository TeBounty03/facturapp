# services/invoice_service.py
import sqlite3
import datetime
from facturapp.utils.database import DB_PATH, generate_invoice_number

def save_invoice(customer_id, items, status="Draft"):
    total_general = sum(item[4] for item in items)
    number = generate_invoice_number()
    date = datetime.date.today().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invoices (number, date, customer_id, total, status)
        VALUES (?, ?, ?, ?, ?)
    """, (number, date, customer_id, total_general, status))

    # Get the last inserted invoice ID
    invoice_id = cursor.lastrowid

    for project_id, desc, qty, price, total in items:
        cursor.execute("""
            INSERT INTO items (invoice_id, project_id, description, quantity, unit_price, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (invoice_id, project_id, desc, qty, price, total))

    conn.commit()
    conn.close()
    return number
