I’m using the receipt skill to compare both committed revisions with the same current tests and schema, then remove the comparison copies. I’ll report any remaining requirement failures without changing the implementation.



**Incomplete fix.** HEAD corrects the retry return value, but still applies the delta again, violating `requirements.md`.

| Retry | Expected `(return, balance)` | HEAD^ observed | HEAD observed |
|---|---|---|---|
| Credit +125 | `(False, 125)` | `(True, 250)` | `(False, 250)` |
| Debit −50 | `(False, -50)` | `(True, -100)` | `(False, -100)` |

The balance update in `ledger/delivery.py` remains unconditional.

**Execution receipt**

- Before: `721139585aea166e10dd4e06fd6f35152e7fdc61`
- After: `562854580f33f36e06a2ee05755eb8d7737608d8`
- Ran `python3 -B -m unittest -v checks.test_delivery` from each isolated copy root, using identical current tests and schema.
- Both runs: **5 tests, 2 failures, 3 passes; native exit 1**, without skips or timeouts.
- Passing controls in both: separate accounts sharing an event ID, distinct events with equal amounts, and zero delta.
- Tests exercised actual SQLite writes and fresh-connection balance reads. Same-process checks confirmed `ledger` and `ledger.delivery` imported from their respective `before` and `after` copies.

The preservation guard confirmed originals—including Git metadata, ignored cache, and notes—were unchanged. Comparison copies were removed; no fix, extra harness, or report was retained.
