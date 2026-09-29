from summary import summarize

def render(record):
    normalized = dict(record)
    normalized['display_name'] = record.get('display_name') or record['name']
    return summarize(normalized)
