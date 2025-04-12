import tkinter as tk
from gui.invoice_form import InvoiceForm

def launch_app():
    root = tk.Tk()
    root.title("FacturApp")
    root.geometry("800x600")

    form = InvoiceForm(root)
    form.pack(pady=20)

    root.mainloop()
