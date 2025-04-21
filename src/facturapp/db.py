import sqlite3
DB_PATH = "data/invoices.db"

def get_invoice_with_customer(invoice_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            i.number, i.date, i.total, i.status,
            c.name, c.address, c.email
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        WHERE i.id = ?
    """, (invoice_id,))
    
    result = cursor.fetchone()
    conn.close()
    return result

def get_invoice_items(invoice_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            description, quantity, unit_price, total
        FROM items
        WHERE invoice_id = ?
    """, (invoice_id,))
    
    items = cursor.fetchall()
    conn.close()
    return items
