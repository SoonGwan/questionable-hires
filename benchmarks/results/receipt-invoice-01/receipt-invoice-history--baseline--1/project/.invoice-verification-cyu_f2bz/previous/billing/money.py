from decimal import Decimal, ROUND_DOWN

def total(lines, quantum):
    amount = sum((Decimal(row['unit_price']) * row['quantity'] for row in lines), Decimal('0'))
    return str(amount.quantize(Decimal(quantum), rounding=ROUND_DOWN))
