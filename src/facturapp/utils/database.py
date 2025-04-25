import os
import sys
import sqlite3
from pathlib import Path

def get_database_path():
    """Retourne le chemin absolu vers la base de données, même dans un .exe"""
    if getattr(sys, 'frozen', False):  # PyInstaller
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent.parent
    return base_path / "data" / "facturapp.db"

DB_PATH = get_database_path()

def init_db():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Customer table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        street TEXT,
        country TEXT,
        destinataire TEXT,
        email TEXT,
        customer_name TEXT,
        number TEXT
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
        project_id TEXT,
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
    """Generate a unique invoice number based on the current count of invoices in the database.
    The format will be "FAC-XXXX" where XXXX is a zero-padded number.

    Returns:
        _type_: str
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM invoices")
    count = cursor.fetchone()[0] + 1
    conn.close()

    return f"FAC-{count:04d}"

def get_all_customers():
    """ Get all customers from the database.
    Returns a list of tuples containing customer ID and name.

    Returns:
        _type_: list of tuples
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

