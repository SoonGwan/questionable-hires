from adapter import customer_name

def invoice_heading(client, customer_id):
    return customer_name(client, customer_id)
