from company_ledger_runtime import normalize

def amount(value):
    return normalize(value, rounding='half_even')
