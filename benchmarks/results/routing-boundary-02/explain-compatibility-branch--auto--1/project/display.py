def display(record):
    # Compatibility path for records without a name field.
    if 'name' not in record:
        return 'Anonymous'
    return record['name']
