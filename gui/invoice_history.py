import tkinter as tk
from tkinter import ttk
import sqlite3
from models.database import DB_PATH
from services.pdf_generator import generate_invoice_pdf

class InvoiceHistory(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Invoice history")
        self.geometry("600x400")

        self.tree = ttk.Treeview(self, columns=("id", "number", "date", "total", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("number", text="Invoice number")
        self.tree.heading("date", text="Date")
        self.tree.heading("total", text="Total ()")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.column("id", width=0, stretch=False) # Hide ID column
        
        # Button to generate PDF for selected invoice
        btn_pdf = tk.Button(self, text="📄 Print selected invoice", command=self.generate_selected_pdf)
        btn_pdf.pack(pady=10)

        self.load_invoices()

    def load_invoices(self):
        """ Load invoices from the database and display them in the treeview.
        The list is sorted by date in descending order.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT number, date, total, status FROM invoices ORDER BY date DESC")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def generate_selected_pdf(self):
        """ Generate PDF for the selected invoice.
        If no invoice is selected, show a warning message.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Attention”, ”Select an invoice.")
            return

        item = self.tree.item(selected_item)
        values = item["values"]
        invoice_id = values[0]  # Assuming the first column is the ID
        generate_invoice_pdf(invoice_id)
        tk.messagebox.showinfo("Success”, ”Successfully generated PDF !")

