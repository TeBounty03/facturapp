import tkinter as tk
from facturapp.gui.invoice_form import InvoiceForm
from facturapp.gui.customer_form import CustomerForm
from facturapp.gui.invoice_history import InvoiceHistory

def launch_app():
    root = tk.Tk()
    root.title("FacturApp")
    root.geometry("800x800")

    form = InvoiceForm(root)
    form.pack(pady=20)
    
    # Button to open invoice history
    btn_history = tk.Button(root, text="📜 Invoice history", command=InvoiceHistory)
    btn_history.pack(pady=5)
    
    # Button to manage customers
    btn_customers = tk.Button(root, text="👥 Manage customers", command=CustomerForm)
    btn_customers.pack(pady=5)

    root.mainloop()
