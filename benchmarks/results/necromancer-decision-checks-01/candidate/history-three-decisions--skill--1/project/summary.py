def summarize(record):
    code = record.get('code') or 'unknown'
    name = record.get('display_name') or record['name']
    amount = record['amount']
    if amount < 0:
        raise ValueError('negative amount')
    return code, name, amount
