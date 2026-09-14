"""Synthetic native-fixture audit; author solutions are not in the model task."""

PYTHON = '/private/tmp/qh-httpx-preflight.3Slnqw/venv/bin/python'

FILES = {
    'ledger.py': '''import sqlite3


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
''',
    'tests/conftest.py': '''from pathlib import Path
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
''',
    'tests/test_debit.py': '''from ledger import debit


def test_acknowledges_debit(database, amount):
    result = debit(database, "alice", amount)
    assert result == {"debited": True, "account": "alice"}
''',
    'README.md': '''# Local ledger

Authored audit fixture, not a production financial application.
debit(database, account, amount) must persist the balance decrement before
acknowledging it. Another connection opened after the call must observe the new
balance; other accounts remain unchanged. Accounts exist, amounts are positive
integers within the balance. Missing accounts, overdrafts, concurrency, migrations
and monetary representation are outside this ticket.

The native pytest fixtures create a fresh database under the project cwd and
remove it after each case. Preserve both amount cases and native fixture execution.
Run the provided preinstalled Python with -B -m pytest -q -p no:cacheprovider
tests/test_debit.py. No package installation is needed.
''',
}

TASK = '''Audit and improve tests/test_debit.py against the persisted-debit contract
in README.md. Trace the test, native fixtures and actual SQLite transaction.
Determine whether the existing tests catch acknowledging a debit without durably
changing the balance. Use one narrow reachable transaction fault in disposable
project-local copies, preserving the real module and fixture execution. Run both
original amount cases on correct and faulty code and record actual outcomes.
Strengthen the test to check the debited account and unchanged other account from
a new database connection after debit returns, keeping the acknowledgment and
both amount cases. Run both improved cases on correct and faulty code. Report
the detecting assertion with actual/expected values and the limits of the audit.

Use PYTHON_RUNTIME with -B and native pytest (-p no:cacheprovider). No installations,
network, environment changes, unrelated audits, commits or publication. Only
tests/test_debit.py may change in the original project; preserve all other files
and installed skill resources. Do not apply the deliberate fault to the original
implementation. All scratch and mutated copies must stay inside the project and
be removed after use. No separate report file is required.'''.replace('PYTHON_RUNTIME', PYTHON)

CASE = dict(id='sqlite-debit', skill='con-artist', task=TASK, files=FILES)
