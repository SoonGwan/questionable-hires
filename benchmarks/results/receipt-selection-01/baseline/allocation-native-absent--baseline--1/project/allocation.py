def reserve(stock, lines):
    """Return remaining stock; reject invalid/insufficient orders atomically."""
    totals = {}
    for sku, quantity in lines:
        if quantity <= 0 or sku not in stock:
            raise ValueError("invalid order")
        totals[sku] = totals.get(sku, 0) + quantity
    if any(quantity > stock[sku] for sku, quantity in totals.items()):
        raise ValueError("insufficient stock")
    result = dict(stock)
    for sku, quantity in totals.items():
        result[sku] -= quantity
    return result
