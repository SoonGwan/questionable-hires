def customer_name(client, customer_id):
    payload = client.lookup(customer_id)
    return payload['displayName'] if 'displayName' in payload else payload['name']
