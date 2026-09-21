import sqlite3

def append_batch(path, rows):
    connection = sqlite3.connect(path)
    try:
        with connection:
            for key, value in rows:
                connection.execute("INSERT INTO records VALUES (?, ?)", (key, value))
    finally:
        connection.close()
