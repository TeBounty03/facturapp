import unittest
import os
import sqlite3
from models.database import init_db, generate_invoice_number, DB_PATH
from services.invoice_service import create_customer, create_invoice, get_invoice_by_id
from services.pdf_generator import generate_invoice_pdf

class InvoiceTestCase(unittest.TestCase):

    def setUp(self):
        """Créer une base temporaire propre à chaque test"""
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()

    def test_generate_invoice_number(self):
        number = generate_invoice_number()
        self.assertEqual(number, "FAC-0001")

    def test_create_customer(self):
        customer_id = add_customer("John Doe", "1 rue de Paris", "",  "john@example.com", "123456", "FR123")
        self.assertIsInstance(customer_id, int)

    def test_create_invoice_with_items(self):
        customer_id = add_customer("Jane Doe", "2 avenue Victor Hugo", "jane@example.com", "654321", "FR456")
        invoice_id = create_invoice(customer_id, [
            {"description": "Design", "quantity": 2, "unit_price": 300},
            {"description": "Illustration", "quantity": 1, "unit_price": 450}
        ])
        invoice = get_invoice_by_id(invoice_id)
        self.assertEqual(invoice["total"], 1050.0)

    def test_generate_pdf(self):
        customer_id = create_customer("PDF Client", "Rue du PDF", "pdf@example.com", "999", "FR999")
        invoice_id = create_invoice(customer_id, [
            {"description": "Service", "quantity": 1, "unit_price": 1000}
        ])
        filename = generate_invoice_pdf(invoice_id)
        self.assertTrue(os.path.exists(filename))

if __name__ == '__main__':
    unittest.main()
