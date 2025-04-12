import tkinter as tk
from gui.invoice_form import InvoiceForm
from services.pdf_generator import generate_invoice_pdf
from gui.invoice_history import InvoiceHistory

def launch_app():
    root = tk.Tk()
    root.title("FacturApp")
    root.geometry("800x600")

    form = InvoiceForm(root)
    form.pack(pady=20)
    
    # Button to generate PDF for the last invoice
    btn_pdf = tk.Button(root, text="Générer PDF dernière facture", command=lambda: generate_invoice_pdf(1))
    btn_pdf.pack(pady=10)
    
    # Button to open invoice history
    btn_history = tk.Button(root, text="📜 Historique des factures", command=InvoiceHistory)
    btn_history.pack(pady=5)

    root.mainloop()
