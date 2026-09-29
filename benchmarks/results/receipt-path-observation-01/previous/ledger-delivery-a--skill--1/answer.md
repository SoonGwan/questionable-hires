I’ll use the receipt skill to compare HEAD^ and HEAD with the same current tests and schema, record the observed results, and remove the comparison copies without changing originals.

HEAD^ reproduced both defects: the credit retry returned `True` and doubled the balance to 250; the debit retry returned `True` and doubled it to -100. All three controls passed.

The optional assertion observer could not serialize the tests’ `Path` checks, so the helper stopped before HEAD. Its copies were removed and preservation checks passed. I’ll rerun without that optional observer; the unchanged tests directly assert the required return values and balances.

Verified the committed change against the five current tests and stated sequential-delivery scope.

- HEAD^: `721139585aea166e10dd4e06fd6f35152e7fdc61`
- HEAD: `547b2e89c7f99e13192ddc2ccb90f623a8234307`

Both copies ran `python3 -B -m unittest -v checks.test_delivery` with identical current tests and schema, real SQLite writes, and fresh-connection balance reads.

| Check | HEAD^ | HEAD |
|---|---|---|
| Credit retry | Failed: `(True, 250)` | Passed: `(False, 125)` |
| Debit retry | Failed: `(True, -100)` | Passed: `(False, -50)` |
| Same event, different accounts | Passed | Passed |
| Distinct events, equal amounts | Passed | Passed |
| Zero accepted | Passed | Passed |

Native test processes confirmed imports from `.receipt-dmx_tvx2/before/ledger/delivery.py` and `.receipt-dmx_tvx2/after/ledger/delivery.py`, respectively. No tests were skipped.

An initial optional observer failed on `Path` values; the completed comparison used unchanged tests without that observer.

All comparison copies were removed; no harness or report remains. Preservation checks confirmed original bytes/modes, including ignored files and unrelated notes, remained unchanged. No fix was implemented.
