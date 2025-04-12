from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
import sqlite3
import json
import os

from models.database import DB_PATH

CONFIG_PATH = "config/user_config.json"
OUTPUT_DIR = "exports"

def load_company_info():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def generate_invoice_pdf(invoice_id):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Récupération facture
    cursor.execute("""
        SELECT i.number, i.date, i.total, c.name, c.address, c.email
        FROM invoices i
        LEFT JOIN customers c ON i.customer_id = c.id
        WHERE i.id = ?
    """, (invoice_id,))
    invoice = cursor.fetchone()

    if not invoice:
        print("Invoice not found.")
        return

    number, date, total, customer_name, customer_address, customer_email = invoice

    # Récupération des items
    cursor.execute("SELECT description, quantity, unit_price, total FROM items WHERE invoice_id = ?", (invoice_id,))
    items = cursor.fetchall()

    conn.close()

    company = load_company_info()

    # Création du PDF
    pdf_path = f"{OUTPUT_DIR}/{number}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Coordonnées de départ
    x = 20 * mm
    y = height - 30 * mm

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, f"Facture {number}")
    y -= 10 * mm
    c.setFont("Helvetica", 10)
    c.drawString(x, y, f"Date : {date}")
    y -= 15 * mm

    # Infos société
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, company["company_name"])
    y -= 5 * mm
    c.setFont("Helvetica", 10)
    c.drawString(x, y, company["address"])
    y -= 5 * mm
    c.drawString(x, y, company["email"])
    y -= 5 * mm
    c.drawString(x, y, f"SIRET : {company['siret']} | TVA : {company['vat_number']}")
    y -= 10 * mm
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Invoiced to :")
    y -= 5 * mm
    c.setFont("Helvetica", 10)

    if customer_name:
        c.drawString(x, y, customer_name)
        y -= 5 * mm
        if customer_address:
            c.drawString(x, y, customer_address)
            y -= 5 * mm
        if customer_email:
            c.drawString(x, y, customer_email)
            y -= 5 * mm
    else:
        c.drawString(x, y, "Customer not specified")
        y -= 5 * mm


    # Table of items
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, "Description")
    c.drawString(x + 80 * mm, y, "Qty")
    c.drawString(x + 100 * mm, y, "Price/H")
    c.drawString(x + 130 * mm, y, "Total")
    y -= 8 * mm
    c.setFont("Helvetica", 10)

    for desc, qty, unit_price, item_total in items:
        c.drawString(x, y, desc)
        c.drawString(x + 80 * mm, y, str(qty))
        c.drawString(x + 100 * mm, y, f"{unit_price:.2f} €")
        c.drawString(x + 130 * mm, y, f"{item_total:.2f} €")
        y -= 6 * mm

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 100 * mm, y, "Total :")
    c.drawString(x + 130 * mm, y, f"{total:.2f} €")
    
    # Footer (payment info)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)

    payment_text = f"""
    Payment made to:
    Name: {company.get('name', '')} 
    Address : {company.get('address', '')}
    Phone Number: {company.get('phone', '')}
    Email: {company.get('email', '')}
    Your payment information here: {company.get('payment', '')}
    Wire Transfer, E-Transfer, Paypal or Check
    Bank Name: {company.get('bank_name', '')}
    Rounting Number: {company.get('routing_number', '')}
    Bank Number: {company.get('bank_number', '')}
    Account Number: {company.get('account_number', '')}
    IBAN: {company.get('iban', '')}
    Swift Code: {company.get('swift_code', '')}
    """
    text = c.beginText(x, 15 * mm)
    text.textLines(payment_text)
    c.drawText(text)

    c.save()

    print(f"✅ Generated PDF : {pdf_path}")
