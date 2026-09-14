from decimal import Decimal
from amounts import amount_cents


def invoice_total(amount):
    if not isinstance(amount, str):
        raise TypeError("invoice amounts must be decimal strings")
    return amount_cents(Decimal(amount))
