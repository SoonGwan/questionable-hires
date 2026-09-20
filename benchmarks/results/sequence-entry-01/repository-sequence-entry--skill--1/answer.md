I’m using the receipt skill to compare both revisions with the same eight current tests, verify the implementation loaded in each test process, and check that cleanup preserves the workspace.



The fix wakes the entry wait when the component finishes and reports whether it returned, raised, or cancelled. I’ll run the eight selected tests in disposable copies and check `probe.__file__` inside each unittest process; the comparison helper’s module-only check would not verify that attribute.



Verified the existing fix: **HEAD^ had four defect-specific timeout errors; HEAD passed all eight selected tests**, with no skips.

- Before: `7a5c5b0ba9ff661624ec8dd7242563905a8d7b38`
- After: `a8d15369e7d70d98b16f9008e89c2b70eab24d2d`

| Selected behavior | HEAD^ | HEAD |
|---|---|---|
| Return before fetch | TimeoutError | Expected descriptive ValueError |
| Exception before fetch | TimeoutError | ValueError includes `RuntimeError: missing request configuration` |
| Second request returns early | TimeoutError | Expected ValueError; cleanup assertions pass |
| Cancellation before fetch | TimeoutError | Expected cancellation ValueError |
| Cooperative setup | Pass | Pass |
| Genuine timeout and cleanup | Pass | Pass |
| Stale overwrite versus guard | Pass | Pass |
| Normal/boundary and stale guard controls | Pass | Pass |

The four before errors came from expired 0.5-second async waits at `entered.get()`. Neither process had setup/import failures or exceeded its process timeout.

Both runs used Python 3.9.6 at `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`, invoked with `-B -c` and an in-memory unittest runner. Exactly the eight identities from `selected-tests.json` ran against identical current test bytes/modes, with `tests/` as an import root.

Inside each native process, `test_mother_in_law_sequence_probe.probe.__file__` was asserted and printed, resolving under the project to:

- PID 3268: `.receipt-verify-5ky9uxc4/before/skills/mother-in-law/scripts/sequence_probe.py`
- PID 3271: `.receipt-verify-5ky9uxc4/after/skills/mother-in-law/scripts/sequence_probe.py`

All 78 inventoried entries retained their bytes/modes, including Git metadata and `notes.txt`. Git status was unchanged; diff checks passed. Comparison copies were removed, and no harness or report remains. Coverage is limited to the requested eight tests.
