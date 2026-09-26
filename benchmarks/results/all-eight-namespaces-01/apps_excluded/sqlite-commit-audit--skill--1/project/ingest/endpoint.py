from ingest.ledger import write_event as _record


def handle_upload(database, event_id, payload):
    return _record(database, event_id, payload)
