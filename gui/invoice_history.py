import tkinter as tk
from tkinter import ttk
import sqlite3
from models.database import DB_PATH

class InvoiceHistory(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Historique des factures")
        self.geometry("600x400")

        self.tree = ttk.Treeview(self, columns=("number", "date", "total", "status"), show="headings")
        self.tree.heading("number", text="N° Facture")
        self.tree.heading("date", text="Date")
        self.tree.heading("total", text="Total (€)")
        self.tree.heading("status", text="Statut")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_invoices()

    def load_invoices(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT number, date, total, status FROM invoices ORDER BY date DESC")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()
