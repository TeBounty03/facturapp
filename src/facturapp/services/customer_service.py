import sqlite3
from models.database import DB_PATH
from models.customer import Customer
from contextlib import closing

def add_customer(customer: Customer) -> int:
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    INSERT INTO customers (name, street, country, destinataire, number, email)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (customer.name, customer.street, customer.country, customer.destinataire, customer.number, customer.email))
                conn.commit()
                return cursor.lastrowid
    except sqlite3.Error as e:
        raise Exception(f"Client insertion error: {e}")

def get_all_customers() -> list[Customer]:
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT id, name, street, country, destinataire, number, email FROM customers ORDER BY name ASC")
                rows = cursor.fetchall()
                conn.close()
                if not rows:
                    return []
                return [Customer(*row) for row in rows]
    except sqlite3.Error as e:
        raise Exception(f"Error fetching customers: {e}")

def update_customer(customer: Customer) -> bool:
    if not customer.id:
        raise ValueError("Customer ID is required for update.")
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    UPDATE customers
                    SET name = ?, street = ?, country = ?, destinataire = ?, number = ?, email = ?
                    WHERE id = ?
                """, (customer.name, customer.street, customer.country, customer.destinataire, customer.number, customer.email, customer.id))
                conn.commit()
                conn.close()
                return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise Exception(f"Error updating customer: {e}")

def delete_customer_by_id(customer_id):
    if not customer_id:
        raise ValueError("Customer ID is required for deletion.")
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
                conn.commit()
                conn.close()
    except sqlite3.Error as e:
        raise Exception(f"Error deleting customer: {e}")
