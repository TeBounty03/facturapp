import tkinter as tk
import gettext
from models.database import DB_PATH
from tkinter import ttk
from models.database import get_all_customers
from services.invoice_service import save_invoice

_ = gettext.gettext # Translation function


class InvoiceForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.items = []
        
        # Sélection customer
        self.customer_var = tk.StringVar()
        tk.Label(self, text=_("Customer :")).grid(row=0, column=0, sticky="e")
        self.customer_dropdown = ttk.Combobox(self, textvariable=self.customer_var, state="readonly")
        self.customer_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Project ID
        tk.Label(self, text=_("Project ID :")).grid(row=1, column=0, sticky="e")
        self.project_id = tk.Entry(self, width=40)
        self.project_id.grid(row=1, column=1, columnspan=2, pady=5)
        
        # Description
        tk.Label(self, text=_("Description :")).grid(row=2, column=0, sticky="e")
        self.description_entry = tk.Entry(self, width=40)
        self.description_entry.grid(row=2, column=1, columnspan=2, pady=5)

        # Quantity (hours)
        tk.Label(self, text=_("Quantity (h) :")).grid(row=3, column=0, sticky="e")
        self.qty_entry = tk.Entry(self)
        self.qty_entry.grid(row=3, column=1, pady=5)

        # Price per hour
        tk.Label(self, text=_("Price / hours (€) :")).grid(row=4, column=0, sticky="e")
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=4, column=1, pady=5)
        
        # Payment Terms
        tk.Label(self, text=_("Payment Terms :")).grid(row=5, column=0, sticky="e")
        self.payment_terms = tk.Entry(self)
        self.payment_terms.grid(row=5, column=1, pady=5)

        # Button "Add"
        self.add_btn = tk.Button(self, text=_("Add"), command=self.add_item)
        self.add_btn.grid(row=6, column=1, pady=10)
        
        # List of items
        self.tree = ttk.Treeview(self, columns=(_("Project"), _("Description"), _("Quantity"), _("Price"), _("Total")), show="headings")
        for col in ("Project", "Description", "Quantity", "Price", "Total"):
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=100, width=120)
        self.tree.grid(row=7, column=0, columnspan=3, pady=10)
        
        # Total
        self.total_label = tk.Label(self, text="Total : 0.00 €", font=("Arial", 14, "bold"))
        self.total_label.grid(row=8, column=0, columnspan=3, pady=10)
        
        self.save_btn = tk.Button(self, text="Save invoice", command=self.save_invoice, bg="#4CAF50", fg="white")
        self.save_btn.grid(row=9, column=0, columnspan=3, pady=10)

        self.load_customers()


    def add_item(self):
        project = self.project_id.get()
        desc = self.description_entry.get()
        qty = self.qty_entry.get()
        price = self.price_entry.get()

        try:
            qty = int(qty)
            price = float(price)
            total = qty * price
            self.items.append((project, desc, qty, price, total))
            self.tree.insert("", "end", values=(project, desc, qty, f"{price:.2f}", f"{total:.2f}"))

            # Reset fields
            self.project_id.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            
            # Update total label
            total_general = sum(item[3] for item in self.items)
            self.total_label.config(text=f"Total : {total_general:.2f} €")
        except ValueError:
            print("Error: quantity and price fields must be numbers.")
    
    def save_invoice(self):
        if not self.items:
            print("No items to save.")
            return

        customer_name = self.customer_var.get()
        customer_id = self.customers_dict.get(customer_name, None)

        try:
            invoice_number = save_invoice(customer_id, self.items)
            print(f"Invoice {invoice_number} successfully saved ✅")

            self.items.clear()
            self.tree.delete(*self.tree.get_children())
            self.total_label.config(text="Total : 0.00 €")
        except Exception as e:
            print("Error saving invoice:", e)
    
    def load_customers(self):
        customers = get_all_customers()
        self.customers_dict = {name: id_ for id_, name in customers}
        self.customer_dropdown['values'] = list(self.customers_dict.keys())

