def display_label(payload):
    return payload.get('display_name') or payload['name']
