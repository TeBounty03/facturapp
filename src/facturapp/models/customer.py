class Customer:
    def __init__(self, id, name, street, country, destinataire, number, email):
        self.id = id
        self.name = name
        self.street = street
        self.country = country
        self.destinataire = destinataire
        self.number = number
        self.email = email

    def __repr__(self):
        return f"<Customer {self.id} - {self.name}>"
