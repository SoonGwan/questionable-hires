import sqlite3


def debit(database, account, amount):
    connection = sqlite3.connect(database)
    try:
        changed = connection.execute(
            "UPDATE accounts SET balance = balance - ? WHERE name = ?",
            (amount, account),
        ).rowcount
        connection.commit()
        return {"debited": changed == 1, "account": account}
    finally:
        connection.close()
