I’ll inspect Search and the local test setup, then add a deterministic test for both completion orders without changing production code.

`Search.run` assigns each response directly to the displayed result, so an older request appears able to overwrite a newer one. I’ll test that with explicit response gates. The normal-order test will check only the result after both requests finish; the reversed-order test will check that the latest result survives the older response.

The test reproduced the failure: normal completion passes, but releasing `ca` after `cat` replaces the completed latest result with `results for ca`. Both requests were confirmed pending before release, and the reversed-order test verified that `results for cat` was visible before the older response arrived.

Reproduced a stale-response overwrite against actual `Search`.

- Normal completion: passes; latest result remains after both requests finish.
- Reversed completion: fails; older `ca` overwrites completed `cat`.
- Tests use controlled overlapping requests, bounded waits, and owned-task cleanup.

Rerun: `python3 -B -m unittest -v test_search`

Added `test_search.py` and `QA.md` with controls and actual assertion evidence. Production files are unchanged, verified by hashes.
