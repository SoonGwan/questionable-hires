import sqlite3
from contextlib import closing

from ledger import debit


def test_acknowledges_debit(database, amount):
    result = debit(database, "alice", amount)
    assert result == {"debited": True, "account": "alice"}

    with closing(sqlite3.connect(database)) as connection:
        balances = dict(connection.execute("SELECT name, balance FROM accounts"))

    assert balances["alice"] == 100 - amount
    assert balances["bob"] == 250
