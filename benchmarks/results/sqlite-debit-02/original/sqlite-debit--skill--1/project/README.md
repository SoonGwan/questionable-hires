# Local ledger

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
