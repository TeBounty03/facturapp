import sqlite3
from models.database import DB_PATH
from models.customer import Customer
from tkinter import messagebox 

def add_customer(customer: Customer):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO customers (name, street, country, destinataire, number, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer.name, customer.street, customer.country, customer.destinataire, customer.number, customer.email))
    conn.commit()
    conn.close()

def get_all_customers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, street, country, destinataire, number, email FROM customers ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return [Customer(*row) for row in rows]

def update_customer(customer: Customer):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE customers
        SET name = ?, street = ?, country = ?, destinataire = ?, number = ?, email = ?
        WHERE id = ?
    """, (customer.name, customer.street, customer.country, customer.destinataire, customer.number, customer.email, customer.id))
    updated = cursor.rowcount
    conn.commit()
    conn.close()
    return updated > 0


def delete_customer_by_id(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
