from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
import sqlite3
import json
import os

from models.database import DB_PATH
from services.db import get_invoice_with_customer, get_invoice_items

CONFIG_PATH = "config/user_config.json"
OUTPUT_DIR = "exports"
LOGO_PATH = "assets/logo_example.jpg"

def load_company_info():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def generate_invoice_pdf(invoice_id):
    company = load_company_info()
    invoice_data = get_invoice_with_customer(invoice_id)
    if invoice_data is None:
        print(f"❌ No invoice found with ID {invoice_id}")
        return
    items = get_invoice_items(invoice_id)

    number, date_str, total, status, customer_name, customer_address, customer_email = invoice_data

    os.makedirs("invoices", exist_ok=True)
    filename = f"invoices/Invoice_{number}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin_x, margin_y = 20 * mm, 20 * mm
    y = height - margin_y

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin_x, margin_y = 20 * mm, 20 * mm
    y = height - margin_y

    # LOGO (à droite)
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, width - margin_x - 40*mm, y - 25, width=50*mm, height=30*mm, preserveAspectRatio=True)
    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin_x, y, f"INVOICE ID # {number}")
    c.setFont("Helvetica", 12)
    c.drawString(margin_x, y - 20, f"DATE: {date_str}")
    y -= 40

    # Ligne de séparation
    c.line(margin_x, y, width - margin_x, y)
    y -= 20

    # Customer info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, y, "Customer:")
    c.setFont("Helvetica", 10)
    y -= 15
    c.drawString(margin_x, y, customer_name or "")
    y -= 15
    c.drawString(margin_x, y, customer_address or "")
    y -= 15
    if customer_email:
        c.drawString(margin_x, y, customer_email)
        y -= 15
    
    # Ligne de séparation
    y -= 10
    c.line(margin_x, y, width - margin_x, y)
    y -= 20

    # Table header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_x, y, "Description")
    c.drawString(margin_x + 100*mm, y, "Qty")
    c.drawString(margin_x + 120*mm, y, "PU €")
    c.drawString(margin_x + 140*mm, y, "Total €")
    y -= 15
    c.line(margin_x, y, width - margin_x, y)
    y -= 10

    # Items
    c.setFont("Helvetica", 9)
    for item in items:
        description, quantity, unit_price, total_item = item
        c.drawString(margin_x, y, description)
        c.drawString(margin_x + 100*mm, y, str(quantity))
        c.drawString(margin_x + 120*mm, y, f"{unit_price:.2f}")
        c.drawString(margin_x + 140*mm, y, f"{total_item:.2f}")
        y -= 15

    # Ligne de séparation
    y -= 10
    c.line(margin_x, y, width - margin_x, y)
    y -= 20

    # Payment info
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_x, y, "Payment made to:")
    y -= 15
    c.setFont("Helvetica", 9)
    c.drawString(margin_x, y, f"Name: {company['name']}")
    y -= 12
    c.drawString(margin_x, y, f"Address: {company['address']}")
    y -= 12
    c.drawString(margin_x, y, f"Phone number: {company['phone']}")
    y -= 12
    c.drawString(margin_x, y, f"Email address: {company['email']}")
    y -= 12
    c.drawString(margin_x, y, "Your payment information here: Wire Transfer")
    y -= 12
    c.drawString(margin_x, y, "Wire Transfer, E-Transfer, Paypal or Check")
    y -= 20

    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(width - margin_x, y, f"TOTAL : {total:.2f} €")

    c.save()
    print(f"✅ Invoice generated: {filename}")