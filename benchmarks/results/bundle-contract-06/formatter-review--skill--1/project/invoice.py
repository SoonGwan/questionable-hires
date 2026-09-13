from formatting import registry

def total_label(cents):
    return registry.format('usd', cents)
