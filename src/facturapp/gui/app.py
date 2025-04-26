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

    root.mainloop()
