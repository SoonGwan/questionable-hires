from pathlib import Path
import sqlite3
import tempfile
import pytest


@pytest.fixture
def database():
    with tempfile.TemporaryDirectory(prefix="ledger-test-", dir=Path.cwd()) as folder:
        path = Path(folder) / "ledger.sqlite"
        with sqlite3.connect(path) as connection:
            connection.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER)")
            connection.executemany("INSERT INTO accounts VALUES (?, ?)", [("alice", 100), ("bob", 250)])
        yield path


@pytest.fixture(params=[7, 13], ids=["small", "larger"])
def amount(request):
    return request.param
