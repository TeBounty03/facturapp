import tkinter as tk
import sys
import os
from facturapp.gui.invoice_form import InvoiceForm
from facturapp.gui.customer_form import CustomerForm
from facturapp.utils.database import init_db


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
init_db()  # Initialize the database if it doesn't exist


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Facturapp")
        
        # Création du formulaire de facture
        self.invoice_form = InvoiceForm(self)
        self.invoice_form.pack(fill=tk.BOTH, expand=True)
        
        # Bouton pour ouvrir le formulaire client
        tk.Button(
            self,
            text="Gérer Clients",
            command=self.open_customer_form
        ).pack(pady=10)

    def open_customer_form(self):
        """Ouvre le formulaire client avec callback de rafraîchissement"""
        CustomerForm(
            master=self,
            refresh_callback=self.invoice_form.load_customers  # Important!
        )

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Facturapp")
        
        # Création du formulaire de facture
        self.invoice_form = InvoiceForm(self)
        self.invoice_form.pack(fill=tk.BOTH, expand=True)
        
        # Bouton pour ouvrir le formulaire client
        tk.Button(
            self,
            text="Gérer Clients",
            command=self.open_customer_form
        ).pack(pady=10)

    def open_customer_form(self):
        """Ouvre le formulaire client avec callback de rafraîchissement"""
        CustomerForm(
            master=self,
            refresh_callback=self.invoice_form.load_customers  # Important!
        )

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()