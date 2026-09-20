I’m using the receipt skill to compare both revisions with the same current tests and schema, check which code each run loads, and report any remaining failures without changing the originals.

The commit changes the return value, but still updates the balance on every retry. The five current tests use real SQLite writes and fresh connections for balance reads; I’ll run them unchanged against both revisions to confirm the effect.

**The committed fix is incomplete.** Retries now return `False`, but still apply the delta again, violating `requirements.md`.

Ran `python3 -B -m unittest -v checks.test_delivery` from each isolated copy root with identical current tests and schema, using real SQLite writes and fresh-connection reads.

| Retry result `(accepted, balance)` | HEAD^ | HEAD | Required |
|---|---|---|---|
| Credit +125 | `(True, 250)` | `(False, 250)` | `(False, 125)` |
| Debit −50 | `(True, -100)` | `(False, -100)` | `(False, -50)` |

Both runs: **5 tests, 2 failures, 3 passes**, exit code 1. Controls passed for independent accounts, distinct events with equal amounts, and zero delta.

Loaded revisions:
- HEAD^: `721139585aea166e10dd4e06fd6f35152e7fdc61`
- HEAD: `562854580f33f36e06a2ee05755eb8d7737608d8`

Same-process import checks confirmed `ledger.delivery` loaded from `.receipt-wb8d3t2g/before/ledger/delivery.py` and `.receipt-wb8d3t2g/after/ledger/delivery.py`, respectively.

The balance `UPDATE` remains unconditional. No fix was made. Preservation checks confirmed originals—including Git metadata, ignored cache, and user notes—unchanged. Test cleanup ran normally; comparison copies were removed, with no harness or report retained.
