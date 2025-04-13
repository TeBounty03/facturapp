from db import get_invoice_with_customer

invoice_id = 1  # Ou un ID réel dans ta base

result = get_invoice_with_customer(invoice_id)
print("Résultat:", result)
