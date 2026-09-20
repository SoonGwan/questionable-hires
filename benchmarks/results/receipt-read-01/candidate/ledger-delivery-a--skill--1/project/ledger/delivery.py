import sqlite3
from contextlib import closing

def apply_event(path, account, event, cents):
    with closing(sqlite3.connect(path)) as db, db:
        inserted = db.execute('INSERT OR IGNORE INTO seen VALUES (?, ?)', (account, event)).rowcount
        if not inserted:
            return False
        db.execute('UPDATE accounts SET cents = cents + ? WHERE id = ?', (cents, account))
        return True
