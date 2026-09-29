I’m using the receipt skill to compare the committed versions with the same current tests and schema. I’ll check the loaded code, report any remaining failures, and remove the comparison copies without changing originals.


The comparison shows the fix works for all five current tests. Before the change, credit and debit retries applied twice; after it, both return `False` and preserve the balance. All three controls pass on both revisions, and each test process loaded its copy-local implementation.


Verified the committed duplicate-delivery fix against `requirements.md` within its stated sequential-call scope.

Compared:
- HEAD^: `721139585aea166e10dd4e06fd6f35152e7fdc61`
- HEAD: `547b2e89c7f99e13192ddc2ccb90f623a8234307`

Ran `python3 -B -m unittest -v checks.test_delivery` from each isolated copy root, using identical current tests and schema, actual SQLite writes, and fresh-connection balance reads.

| Test | HEAD^ | HEAD |
|---|---|---|
| Credit retry | Failed: `(True, 250)` | Passed: `(False, 125)` |
| Debit retry | Failed: `(True, -100)` | Passed: `(False, -50)` |
| Same event, different accounts | Passed | Passed |
| Distinct events, equal amounts | Passed | Passed |
| Zero delta | Passed | Passed |

All five tests ran without skips. Native processes confirmed `ledger.delivery` and test imports under `.receipt-8zyz3fpt/before/` and `/after/`, respectively.

The change returns `False` before updating balances when the account/event pair already exists. All originals—including ignored cache, Git metadata and modified notes—passed preservation checks. Comparison copies were removed; no test databases, extra harness or report remain.
