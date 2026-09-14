import sqlite3

from ledger import debit


def test_acknowledges_debit(database, amount):
    result = debit(database, "alice", amount)
    assert result == {"debited": True, "account": "alice"}

    connection = sqlite3.connect(database)
    try:
        balances = dict(connection.execute("SELECT name, balance FROM accounts"))
    finally:
        connection.close()

    assert balances["alice"] == 100 - amount
    assert balances["bob"] == 250
