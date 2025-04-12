import tkinter as tk
from tkinter import ttk

class InvoiceForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.items = []

        # Description
        tk.Label(self, text="Description :").grid(row=0, column=0, sticky="e")
        self.description_entry = tk.Entry(self, width=40)
        self.description_entry.grid(row=0, column=1, columnspan=2, pady=5)

        # Quantité (heures)
        tk.Label(self, text="Quantité (h) :").grid(row=1, column=0, sticky="e")
        self.qty_entry = tk.Entry(self)
        self.qty_entry.grid(row=1, column=1, pady=5)

        # Prix par heure
        tk.Label(self, text="Prix / heure (€) :").grid(row=2, column=0, sticky="e")
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=2, column=1, pady=5)

        # Bouton "Ajouter"
        self.add_btn = tk.Button(self, text="Ajouter", command=self.add_item)
        self.add_btn.grid(row=3, column=1, pady=10)

        # Liste des items
        self.tree = ttk.Treeview(self, columns=("Description", "Quantité", "Prix", "Total"), show="headings")
        for col in ("Description", "Quantité", "Prix", "Total"):
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=100, width=120)
        self.tree.grid(row=4, column=0, columnspan=3, pady=10)

    def add_item(self):
        desc = self.description_entry.get()
        qty = self.qty_entry.get()
        price = self.price_entry.get()

        try:
            qty = int(qty)
            price = float(price)
            total = qty * price
            self.items.append((desc, qty, price, total))
            self.tree.insert("", "end", values=(desc, qty, f"{price:.2f}", f"{total:.2f}"))

            # Reset fields
            self.description_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        except ValueError:
            print("Error: quantity and price fields must be numbers.")
