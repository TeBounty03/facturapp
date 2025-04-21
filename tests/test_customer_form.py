import unittest
import tkinter as tk
from gui.customer_form import CustomerForm

class TestCustomerManager(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # cache la fenêtre principale
        self.app = CustomerForm()

    def tearDown(self):
        self.app.destroy()
        self.root.destroy()

    def test_form_fields_exist(self):
        self.assertTrue(hasattr(self.app, 'name_var'))
        self.assertTrue(hasattr(self.app, 'street_var'))
        self.assertTrue(hasattr(self.app, 'country_var'))
        self.assertTrue(hasattr(self.app, 'destinataire_var'))
        self.assertTrue(hasattr(self.app, 'number_var'))
        self.assertTrue(hasattr(self.app, 'email_var'))
        self.assertIsInstance(self.app.customer_list, tk.Listbox)

    def test_add_customer_empty_name(self):
        self.app.name_var.set("")
        with self.assertRaises(tk.TclError):  # messagebox showerror stoppe ici
            self.app.add_customer()

    def test_reset_form(self):
        self.app.name_var.set("Test")
        self.app._reset_form()
        self.assertEqual(self.app.name_var.get(), "")

if __name__ == '__main__':
    unittest.main()
