import sqlite3


def write_event(database, event_id, payload):
    connection = sqlite3.connect(database)
    try:
        connection.execute('INSERT INTO events (id, payload) VALUES (?, ?)',
                           (event_id, payload))
        connection.commit()
    finally:
        connection.close()
    return {'accepted': event_id}
