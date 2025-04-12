import sqlite3
import os
import datetime

DB_PATH = "data/invoices.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Customer table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        email TEXT,
        siret TEXT,
        vat_number TEXT
    )
    """)

    # Invoice table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT,
        date TEXT,
        customer_id INTEGER,
        total REAL,
        status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    # Table items (invoice details)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        description TEXT,
        quantity INTEGER,
        unit_price REAL,
        total REAL,
        FOREIGN KEY(invoice_id) REFERENCES invoices(id)
    )
    """)

    conn.commit()
    conn.close()
    
def generate_invoice_number():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM invoices")
    count = cursor.fetchone()[0] + 1
    conn.close()

    return f"FAC-{count:04d}"

def get_all_customers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

