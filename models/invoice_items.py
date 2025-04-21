# models/item.py
class InvoiceItem:
    def __init__(self, description, quantity, unit_price):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.total = quantity * unit_price
