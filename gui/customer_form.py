import tkinter as tk
from tkinter import messagebox
from models.customer import Customer
from services.customer_service import add_customer, get_all_customers, update_customer, delete_customer_by_id
import re # For email validation

class CustomerForm(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Customer management")
        self.geometry("400x500")
        
        # Configuration pour rester au premier plan
        self.attributes('-topmost', True)  # Force à rester devant
        self.grab_set()  # Bloque les autres fenêtres
        self.transient(master)  # Lien avec la fenêtre parente

        self.editing_customer_id = None

        # Variables
        self.name_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.destinataire_var = tk.StringVar()
        self.number_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # UI Fields
        tk.Label(self, text="Name :").pack()
        self.name_entry = tk.Entry(self, textvariable=self.name_var)
        self.name_entry.pack()

        tk.Label(self, text="Street :").pack()
        self.street_entry = tk.Entry(self, textvariable=self.street_var)
        self.street_entry.pack()

        tk.Label(self, text="Country :").pack()
        self.country_entry = tk.Entry(self, textvariable=self.country_var)
        self.country_entry.pack()

        tk.Label(self, text="Destinataire :").pack()
        self.destinataire_entry = tk.Entry(self, textvariable=self.destinataire_var)
        self.destinataire_entry.pack()

        tk.Label(self, text="Number :").pack()
        self.number_entry = tk.Entry(self, textvariable=self.number_var)
        self.number_entry.pack()
        # Validation to authorize numbers only
        vcmd = (self.register(self.validate_number), '%P')
        self.number_entry.config(validate="key", validatecommand=vcmd)

        tk.Label(self, text="Email :").pack()
        self.email_entry = tk.Entry(self, textvariable=self.email_var)
        self.email_entry.pack()

        # Buttons
        self.add_btn = tk.Button(self, text="Add customer", command=self.add_customer)
        self.add_btn.pack(pady=5)

        self.update_btn = tk.Button(self, text="Update customer", command=self.update_customer, state=tk.DISABLED)
        self.update_btn.pack(pady=5)

        self.cancel_btn = tk.Button(self, text="Cancel", command=self._reset_form, state=tk.DISABLED)
        self.cancel_btn.pack(pady=5)
        
        self.delete_btn = tk.Button(self, text="Delete", command=self.delete_customer, state=tk.DISABLED)
        self.delete_btn.pack(pady=5)

        # Customer list
        self.customer_list = tk.Listbox(self)
        self.customer_list.pack(fill=tk.BOTH, expand=True, pady=10)
        self.customer_list.bind("<Double-Button-1>", self.select_customer)
        self.customer_list.bind("<Delete>", self.delete_customer)

        self.load_customers()
        self._keep_on_top()  # Active le maintien au premier plan
    
    def validate_number(self, new_value):
        """Validates that the number field contains digits only"""
        if new_value == "" or new_value.isdigit():
            return True
        return False

    def validate_email(self, email):
        """Validates email format with a regular expression"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_fields(self):
        valid = True
        fields = [
            (self.name_var, self.name_entry),
            (self.street_var, self.street_entry),
            (self.country_var, self.country_entry),
            (self.destinataire_var, self.destinataire_entry),
            (self.number_var, self.number_entry),
            (self.email_var, self.email_entry),
        ]
        
        # Validation des champs vides
        for var, entry in fields:
            if not var.get().strip():
                entry.config(highlightthickness=2, highlightbackground="red")
                valid = False
            else:
                entry.config(highlightthickness=0)
        
        # Validation spécifique pour l'email
        if self.email_var.get().strip() and not self.validate_email(self.email_var.get().strip()):
            self.email_entry.config(highlightthickness=2, highlightbackground="red")
            self.show_warning("Incorrect format", "Please enter a valid email address (e.g. exemple@domaine.com)")
            valid = False
        else:
            self.email_entry.config(highlightthickness=0)
        
        return valid

    def add_customer(self):
        if not self.validate_fields():
            return

        customer = Customer(
            id=None,
            name=self.name_var.get(),
            street=self.street_var.get(),
            country=self.country_var.get(),
            destinataire=self.destinataire_var.get(),
            number=self.number_var.get(),
            email=self.email_var.get(),
        )

        add_customer(customer)
        self._reset_form()
        self.load_customers()
        messagebox.showinfo("Success", "Customer added successfully", parent=self)

    def select_customer(self, event):
        selected = self.customer_list.get(tk.ACTIVE)
        if not selected:
            return
        customer_id = selected.split(" - ")[0]
        customers = get_all_customers()
        for c in customers:
            if str(c.id) == customer_id:
                self.name_var.set(c.name)
                self.street_var.set(c.street)
                self.country_var.set(c.country)
                self.destinataire_var.set(c.destinataire)
                self.number_var.set(c.number)
                self.email_var.set(c.email)
                self.editing_customer_id = c.id
                self.update_btn.config(state=tk.NORMAL)
                self.cancel_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)
                self.add_btn.config(state=tk.DISABLED)
                break

    def update_customer(self):
        if not self.editing_customer_id or not self.validate_fields():
            return

        customer = Customer(
            id=self.editing_customer_id,
            name=self.name_var.get(),
            street=self.street_var.get(),
            country=self.country_var.get(),
            destinataire=self.destinataire_var.get(),
            number=self.number_var.get(),
            email=self.email_var.get()
        )

        update_customer(customer)
        messagebox.showinfo("Success", "Customer updated successfully", parent=self)
        self._reset_form()
        self.load_customers()

    def delete_customer(self):
        self._keep_on_top() # Keep the window on top during deletion confirmation
        selected = self.customer_list.get(tk.ACTIVE)
        if not selected:
            return
        customer_id = selected.split(" - ")[0]
        if messagebox.askyesno("Delete", "Delete this customer?", parent=self):
            delete_customer_by_id(customer_id)
            self.load_customers()
        self.focus_force() # Re-focus on the main window

    def load_customers(self):
        self.customer_list.delete(0, tk.END)
        for customer in get_all_customers():
            self.customer_list.insert(tk.END, f"{customer.id} - {customer.name}")

    def _reset_form(self):
        for var in [self.name_var, self.street_var, self.country_var, self.destinataire_var, self.number_var, self.email_var]:
            var.set("")

        for entry in [self.name_entry, self.street_entry, self.country_entry, self.destinataire_entry, self.number_entry, self.email_entry]:
            entry.config(highlightthickness=0)

        self.editing_customer_id = None
        self.update_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.NORMAL)
    
    def show_warning(self, title, message):
        """Displays an error message without closing the parent window."""
        warning = tk.Toplevel(self)
        warning.title(title)
        warning.geometry("500x100")
        warning.resizable(False, False)
        
        tk.Label(warning, text=message, padx=10, pady=10).pack()
        tk.Button(warning, text="OK", command=warning.destroy).pack(pady=5)
        
        # Makes the window modal (blocks interaction with the parent window)
        warning.grab_set()
        self.wait_window(warning)  # Waits for user to close alert
    
    def _keep_on_top(self):
        """Force la fenêtre à rester au premier plan"""
        self.lift()
        self.attributes('-topmost', True)
        self.after(100, self._keep_on_top)  # Vérifie toutes les 100ms