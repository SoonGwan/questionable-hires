from decimal import Decimal, ROUND_HALF_UP

def cents(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
