import tkinter as tk
from tkinter import messagebox
import sqlite3
from models.database import DB_PATH

class CustomerManager(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Customer management")
        self.geometry("400x400")

        self.name_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.destinataire_var = tk.StringVar()
        self.number_var = tk.StringVar()
        self.email_var = tk.StringVar()

        tk.Label(self, text="Name :").pack()
        tk.Entry(self, textvariable=self.name_var).pack()

        tk.Label(self, text="Street :").pack()
        tk.Entry(self, textvariable=self.street_var).pack()
        
        tk.Label(self, text="Country :").pack()
        tk.Entry(self, textvariable=self.country_var).pack()
        
        tk.Label(self, text="Destinataire :").pack()
        tk.Entry(self, textvariable=self.destinataire_var).pack()

        tk.Label(self, text="Number :").pack()
        tk.Entry(self, textvariable=self.number_var).pack()
        
        tk.Label(self, text="Email :").pack()
        tk.Entry(self, textvariable=self.email_var).pack()

        tk.Button(self, text="Add customer", command=self.add_customer).pack(pady=10)

        self.customer_list = tk.Listbox(self)
        self.customer_list.pack(fill=tk.BOTH, expand=True, pady=10)
        self.customer_list.bind("<Double-Button-1>", self.delete_customer)

        self.load_customers()

    def add_customer(self):
        """ Add a new customer to the database and refresh the listbox.
        If the name is empty, show an error message.
        """
        name = self.name_var.get()
        street = self.street_var.get()
        country = self.country_var.get()
        destinataire = self.destinataire_var.get()
        number = self.number_var.get()
        email = self.email_var.get()

        if not name:
            messagebox.showerror("Error”, ”Name is mandatory")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, street, country, destinataire, number, email) VALUES (?, ?, ?, ?, ?, ?)", (name, street, country, destinataire, number, email))
        conn.commit()
        conn.close()

        self.name_var.set("")
        self.street_var.set("")
        self.country_var.set("")
        self.destinataire_var.set("")
        self.number_var.set("")
        self.email_var.set("")

        self.load_customers()

    def load_customers(self):
        """ Load customers from the database and display them in the listbox.
        The list is sorted by name in ascending order.
        """
        self.customer_list.delete(0, tk.END)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM customers ORDER BY name ASC")
        for id_, name in cursor.fetchall():
            self.customer_list.insert(tk.END, f"{id_} - {name}")
        conn.close()

    def delete_customer(self, event):
        """ Delete the selected customer from the database.
        If no customer is selected, do nothing.

        Args:
            event (_type_): _Description of parameter `event`.
        """
        selected = self.customer_list.get(tk.ACTIVE)
        if not selected:
            return
        customer_id = selected.split(" - ")[0]
        if messagebox.askyesno("Delete”, ”Delete this customer?"):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            conn.commit()
            conn.close()
            self.load_customers()
