import sqlite3
from facturapp.utils.database import DB_PATH
from facturapp.models.customer import Customer
from contextlib import closing

def add_customer(customer: Customer) -> int:
    """Ajoute un nouveau client et retourne son ID"""
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    INSERT INTO customers (name, street, country, destinataire, number, email)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (customer.name, customer.street, customer.country, 
                     customer.destinataire, customer.number, customer.email))
                conn.commit()
                return cursor.lastrowid
    except sqlite3.Error as e:
        raise Exception(f"Erreur d'ajout client: {e}")

def get_all_customers() -> list[Customer]:
    """Récupère tous les clients complets en tant qu'objets Customer."""
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT id, name, street, country, destinataire, number, email FROM customers ORDER BY name ASC")
                rows = cursor.fetchall()
                return [Customer(*row) for row in rows]
    except sqlite3.Error as e:
        raise Exception(f"Erreur de récupération clients: {e}")

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
    except sqlite3.Error as e:
        raise Exception(f"Error deleting customer: {e}")
