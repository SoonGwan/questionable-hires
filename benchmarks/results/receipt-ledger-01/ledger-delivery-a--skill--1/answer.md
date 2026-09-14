I’m using the receipt skill to compare the committed change against its parent with the same current tests and schema. I’ll preserve the originals, check real SQLite behavior and copy-local imports, then remove the comparison copies.



The change skips the balance update when SQLite rejects a duplicate `(account, event)` insert. The five current tests cover credit and debit retries plus three controls, using real writes and fresh-connection reads. I’ll adapt the comparison helper in memory to run the exact requested command and capture import paths without changing any files.



Verified for the documented scope: the committed change satisfies `requirements.md`.

Both isolated copies ran `python3 -B -m unittest -v checks.test_delivery` with identical current tests and schema, real SQLite writes, and fresh-connection balance reads.

| Check | HEAD^ | HEAD |
|---|---|---|
| Credit retry | Failed: `(True, 250)` | Passed: `(False, 125)` |
| Debit retry | Failed: `(True, -100)` | Passed: `(False, -50)` |
| Same event, different accounts | Passed | Passed |
| Distinct events, equal amounts | Passed | Passed |
| Zero accepted | Passed | Passed |

Loaded revisions:

- Before: `721139585aea166e10dd4e06fd6f35152e7fdc61` — 2 failures, exit 1.
- After: `547b2e89c7f99e13192ddc2ccb90f623a8234307` — all 5 passed, exit 0.

Native import traces confirmed `ledger/delivery.py` loaded from each respective `.receipt-2wf285a_/{before,after}/` copy.

Test databases cleaned up normally. Comparison copies were removed; no harness or report remains. Whole-project preservation checks passed, including ignored files and unrelated notes. `git diff --check` passed.
