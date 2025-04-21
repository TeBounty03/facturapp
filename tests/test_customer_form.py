import pytest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from models.customer import Customer
from services.customer_service import add_customer
from gui.customer_form import CustomerForm  # Remplacez par le bon chemin d'import

class TestCustomerForm:
    """Tests unitaires pour la classe CustomerForm"""
    
    @pytest.fixture
    def mock_form(self):
        """Fixture pour créer une instance mockée de CustomerForm"""
        with patch('tkinter.Tk'), patch('tkinter.Toplevel'):
            form = CustomerForm()
            form.master = MagicMock()
            yield form
    
    def test_initial_state(self, mock_form):
        """Teste l'état initial du formulaire"""
        assert mock_form.editing_customer_id is None
        assert mock_form.add_btn['state'] == 'normal'
        assert mock_form.update_btn['state'] == 'disabled'
        assert mock_form.cancel_btn['state'] == 'disabled'
        assert mock_form.delete_btn['state'] == 'disabled'
    
    def test_validate_number(self, mock_form):
        """Teste la validation des numéros"""
        assert mock_form.validate_number("12345") is True
        assert mock_form.validate_number("") is True
        assert mock_form.validate_number("abc") is False
        assert mock_form.validate_number("123a") is False
    
    def test_validate_email(self, mock_form):
        """Teste la validation des emails"""
        assert mock_form.validate_email("test@example.com") is True
        assert mock_form.validate_email("user.name+tag@domain.co.uk") is True
        assert mock_form.validate_email("invalid") is False
        assert mock_form.validate_email("missing@dot") is False
        assert mock_form.validate_email("wrong@.com") is False
    
    @patch('services.customer_service.add_customer')
    def test_add_customer_success(self, mock_add, mock_form):
        """Teste l'ajout réussi d'un client"""
        # Configuration des entrées
        mock_form.name_var.set("John Doe")
        mock_form.street_var.set("123 Main St")
        mock_form.country_var.set("France")
        mock_form.destinataire_var.set("Recipient")
        mock_form.number_var.set("1234567890")
        mock_form.email_var.set("john@example.com")
        
        # Mock de la fonction add_customer
        mock_add.return_value = 42  # Simule un ID retourné
        
        # Mock de messagebox
        with patch.object(messagebox, 'showinfo') as mock_msg:
            mock_form.add_customer()
            
            # Vérifications
            mock_add.assert_called_once()
            called_customer = mock_add.call_args[0][0]
            assert called_customer.name == "John Doe"
            mock_msg.assert_called_once_with(
                "Success, Customer 42 added successfully",
                parent=mock_form
            )
    
    @patch('services.customer_service.add_customer')
    def test_add_customer_validation_failure(self, mock_add, mock_form):
        """Teste l'échec de validation avant ajout"""
        # Configuration d'une entrée invalide (email)
        mock_form.name_var.set("John Doe")
        mock_form.email_var.set("invalid-email")
        
        # Mock de messagebox
        with patch.object(messagebox, 'showwarning') as mock_msg:
            mock_form.add_customer()
            
            # Vérifications
            mock_add.assert_not_called()
            mock_msg.assert_called_once()
    
    @patch('services.customer_service.add_customer')
    def test_add_customer_service_failure(self, mock_add, mock_form):
        """Teste l'échec lors de l'appel au service"""
        # Configuration des entrées valides
        mock_form.name_var.set("John Doe")
        mock_form.street_var.set("123 Main St")
        mock_form.country_var.set("France")
        mock_form.destinataire_var.set("Recipient")
        mock_form.number_var.set("1234567890")
        mock_form.email_var.set("john@example.com")
        
        # Simulation d'une exception
        mock_add.side_effect = Exception("DB error")
        
        # Mock de messagebox
        with patch.object(messagebox, 'showwarning') as mock_msg:
            mock_form.add_customer()
            
            # Vérifications
            mock_add.assert_called_once()
            mock_msg.assert_called_once_with(
                "Error, Customer None already exists",
                parent=mock_form
            )
    
    def test_validate_fields(self, mock_form):
        """Teste la validation des champs du formulaire"""
        # Test avec champs vides
        valid, email_valid = mock_form.validate_fields()
        assert valid is False
        assert email_valid is True
        
        # Test avec email invalide
        mock_form.name_var.set("Name")
        mock_form.street_var.set("Street")
        mock_form.country_var.set("Country")
        mock_form.destinataire_var.set("Dest")
        mock_form.number_var.set("123")
        mock_form.email_var.set("bad-email")
        
        valid, email_valid = mock_form.validate_fields()
        assert valid is True
        assert email_valid is False
        
        # Test avec tout valide
        mock_form.email_var.set("good@email.com")
        valid, email_valid = mock_form.validate_fields()
        assert valid is True
        assert email_valid is True