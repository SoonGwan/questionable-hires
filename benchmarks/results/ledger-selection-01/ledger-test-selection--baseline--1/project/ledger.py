import sqlite3


def transfer(path, source, destination, amount):
    if amount <= 0 or source == destination:
        raise ValueError('invalid transfer')
    connection = sqlite3.connect(path)
    try:
        connection.execute('BEGIN IMMEDIATE')
        changed = connection.execute(
            'UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?',
            (amount, source, amount))
        if changed.rowcount != 1:
            raise ValueError('source unavailable')
        changed = connection.execute(
            'UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, destination))
        if changed.rowcount != 1:
            raise LookupError('destination missing')
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
    finally:
        connection.close()
