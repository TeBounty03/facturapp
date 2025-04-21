import tkinter as tk
from gui.invoice_form import InvoiceForm
from gui.invoice_history import InvoiceHistory
from gui.customer_form import CustomerForm

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
