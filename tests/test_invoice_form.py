import tkinter as tk
import pytest
from unittest.mock import patch, MagicMock
from src.facturapp.gui.invoice_form import InvoiceForm  # Adapte le chemin si besoin

@pytest.fixture
def form():
    # Créer une vraie instance Tk mais la cacher
    root = tk.Tk()
    root.withdraw()
    
    # Configurer les widgets nécessaires pour les tests
    form = InvoiceForm(root)
    form.project_id = tk.Entry(root)  # ou MagicMock() si vous voulez mocker
    form.flid_entry = tk.Entry(root)
    form.description_entry = tk.Entry(root)
    form.qty_entry = tk.Entry(root)
    form.price_entry = tk.Entry(root)
    form.total_label = tk.Label(root)
    form.items = []
    
    yield form
    
    # Nettoyage
    root.destroy()

def test_add_item_valid(form):
    # Simuler une entrée correcte
    form.project_id.insert(0, "Project X")
    form.flid_entry.insert(0, "FLID123")
    form.description_entry.insert(0, "Test description")
    form.qty_entry.insert(0, "5")
    form.price_entry.insert(0, "100")

    form.add_item()

    assert len(form.items) == 1
    assert form.items[0][0] == "Project X"
    assert form.total_label.cget("text") == "Total : 500.00 €"
    print("Test passed: Item added successfully.")

def test_add_item_invalid(form):
    # Simuler une entrée incorrecte
    form.project_id.insert(0, "Project Y")
    form.flid_entry.insert(0, "FLID456")
    form.description_entry.insert(0, "Test description 2")
    form.qty_entry.insert(0, "invalid")  # Valeur invalide
    form.price_entry.insert(0, "100")

    with patch('src.facturapp.gui.invoice_form.InvoiceForm.show_warning') as mock_show_warning:
        form.add_item()
        mock_show_warning.assert_called_once_with("Error", "Invalid input. Please check your values.")
        assert len(form.items) == 0  # Aucun item ne doit être ajouté
        print("Test passed: Invalid input handled correctly.")

def test_save_invoice_no_items(form):
    with patch('src.facturapp.gui.invoice_form.InvoiceForm.show_warning') as mock_show_warning:
        form.save_invoice()
        mock_show_warning.assert_called_once_with("Error", "No items to save.")
        assert len(form.items) == 0  # Aucun item ne doit être ajouté
        print("Test passed: No items to save handled correctly.")

def test_save_invoice_with_items(form):
    # Simuler une entrée correcte
    form.project_id.insert(0, "Project Z")
    form.flid_entry.insert(0, "FLID789")
    form.description_entry.insert(0, "Test description 3")
    form.qty_entry.insert(0, "10")
    form.price_entry.insert(0, "50")

    form.add_item()

    # Mock de la fonction save_invoice
    with patch('src.facturapp.services.invoice_service.save_invoice', return_value="INV-12345") as mock_save_invoice:
        form.save_invoice()
        mock_save_invoice.assert_called_once()
        assert len(form.items) == 0  # Les items doivent être effacés après l'enregistrement
        assert form.total_label.cget("text") == "Total : 0.00 €"
        print("Test passed: Invoice saved successfully.")
