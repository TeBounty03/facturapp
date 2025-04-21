import tkinter as tk
from tkinter import ttk
import sqlite3
from models.database import DB_PATH
from services.pdf_generator import generate_invoice_pdf
from tkinter import messagebox

class InvoiceHistory(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Invoice history")
        self.geometry("700x500")
        self.configure(bg="#f5f5f5")
        
        title_label = tk.Label(self, text="🧾 Invoices", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
        title_label.pack(pady=15)
        
        # Frame pour ajouter du padding autour du tableau
        table_frame = tk.Frame(self, bg="#f5f5f5")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        self.tree = ttk.Treeview(self, columns=("id", "number", "date", "total", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("number", text="Invoice number")
        self.tree.heading("date", text="Date")
        self.tree.heading("total", text="Total (€)")
        self.tree.heading("status", text="Status")
        
        # Largeur des colonnes
        self.tree.column("id", width=0, stretch=False)  # Masquer l'ID
        self.tree.column("number", width=100)
        self.tree.column("date", width=150)
        self.tree.column("total", width=100)
        self.tree.column("status", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bouton pour imprimer
        btn_pdf = tk.Button(
            self,
            text="🖨️ Print selected invoice",
            command=self.generate_selected_pdf,
            bg="#4CAF50", fg="white",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT,
            padx=15, pady=8
        )
        btn_pdf.pack(pady=20)

        self.load_invoices()

    def load_invoices(self):
        """ Load invoices from the database and display them in the treeview.
        The list is sorted by date in descending order.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, number, date, total, status FROM invoices ORDER BY date DESC")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def generate_selected_pdf(self):
        """ Generate PDF for the selected invoice.
        If no invoice is selected, show a warning message.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention”, ”Select an invoice.")
            return

        item = self.tree.item(selected_item)
        values = item["values"]
        invoice_id = values[0]  # Assuming the first column is the ID
        try:
            generate_invoice_pdf(invoice_id)
            messagebox.showinfo("Success", "Successfully generated PDF ✅")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to generate PDF:\n{e}")

