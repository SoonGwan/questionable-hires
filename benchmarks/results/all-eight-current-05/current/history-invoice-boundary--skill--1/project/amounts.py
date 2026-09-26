from decimal import Decimal, ROUND_HALF_UP


def amount_cents(value):
    if isinstance(value, int):
        return value
    return int((Decimal(value) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
