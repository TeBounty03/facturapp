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
    y -= 30  # Plus d'espace avant le tableau
    
    # Définir les dimensions des colonnes
    col_widths = [
        80*mm,  # Description (80mm)
        20*mm,  # Quantité (20mm)
        30*mm,  # Prix unitaire (30mm)
        30*mm   # Total item (30mm)
    ]
    table_width = sum(col_widths)
    table_x = margin_x
    
    # Hauteur des lignes
    row_height = 8*mm
    
    # Table header - dessiner le rectangle d'en-tête
    c.setFillColor(colors.lightgrey)
    c.rect(table_x, y - row_height, table_width, row_height, fill=1, stroke=1)
    c.setFillColor(colors.black)
    
    # Texte de l'en-tête
    c.setFont("Helvetica-Bold", 10)
    header_y = y - row_height + 3*mm  # Position verticale centrée
    
    # Dessiner les bordures verticales et le texte
    c.drawString(table_x + 2*mm, header_y, "Description")
    c.line(table_x + col_widths[0], y - row_height, table_x + col_widths[0], y)
    
    c.drawString(table_x + col_widths[0] + 2*mm, header_y, "Qty")
    c.line(table_x + col_widths[0] + col_widths[1], y - row_height, table_x + col_widths[0] + col_widths[1], y)
    
    c.drawString(table_x + col_widths[0] + col_widths[1] + 2*mm, header_y, "Unit Price")
    c.line(table_x + col_widths[0] + col_widths[1] + col_widths[2], y - row_height, 
           table_x + col_widths[0] + col_widths[1] + col_widths[2], y)
    
    c.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + 2*mm, header_y, "Total")
    
    y -= row_height
    
    # Items - dessiner chaque ligne du tableau
    c.setFont("Helvetica", 9)
    for i, item in enumerate(items):
        description, quantity, unit_price, total_item = item
        
        # Alterner les couleurs de fond pour une meilleure lisibilité
        if i % 2 == 0:
            c.setFillColor(colors.whitesmoke)
        else:
            c.setFillColor(colors.white)
            
        c.rect(table_x, y - row_height, table_width, row_height, fill=1, stroke=1)
        c.setFillColor(colors.black)
        
        # Position verticale centrée pour le texte
        item_y = y - row_height + 3*mm
        
        # Dessiner le texte dans chaque cellule
        c.drawString(table_x + 2*mm, item_y, description[:50])  # Limiter à 50 caractères
        c.drawRightString(table_x + col_widths[0] - 2*mm, item_y, str(quantity))
        c.drawRightString(table_x + col_widths[0] + col_widths[1] - 2*mm, item_y, f"{unit_price:.2f} €")
        c.drawRightString(table_x + col_widths[0] + col_widths[1] + col_widths[2] - 2*mm, item_y, f"{total_item:.2f} €")
        
        # Dessiner les bordures verticales
        c.line(table_x + col_widths[0], y - row_height, table_x + col_widths[0], y)
        c.line(table_x + col_widths[0] + col_widths[1], y - row_height, table_x + col_widths[0] + col_widths[1], y)
        c.line(table_x + col_widths[0] + col_widths[1] + col_widths[2], y - row_height, 
               table_x + col_widths[0] + col_widths[1] + col_widths[2], y)
        
        y -= row_height
    
    # Ligne de séparation après le tableau
    y -= 15
    c.line(margin_x, y, width - margin_x, y)
    y -= 20
    
    # Total - aligné à droite
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - margin_x, y, f"TOTAL : {total:.2f} €")
    y -= 30

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
    c.drawString(margin_x, y, f"Your payment information here: {company['payment']}")
    y -= 12
    c.drawString(margin_x, y, "Wire Transfer, E-Transfer, Paypal or Check")
    y -= 20
    c.drawString(margin_x, y, f"Bank Name: {company['bank_name']}")
    y -= 12
    c.drawString(margin_x, y, f"Routing Number: {company['routing_number']}")
    y -= 12
    c.drawString(margin_x, y, f"Bank Number: {company['bank_number']}")
    y -= 12
    c.drawString(margin_x, y, f"Account Number: {company['account_number']}")
    y -= 12
    c.drawString(margin_x, y, f"IBAN: {company['iban']}")
    y -= 12
    c.drawString(margin_x, y, f"Swift Code: {company['swift_code']}")
    y -= 20

    c.save()
    print(f"✅ Invoice generated: {filename}")