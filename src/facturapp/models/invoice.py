# models/invoice.py
class Invoice:
    def __init__(self, number, date, customer_id, total, status="Draft"):
        self.number = number
        self.date = date
        self.customer_id = customer_id
        self.total = total
        self.status = status
