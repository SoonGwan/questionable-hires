I’ll use the hostage-negotiator skill to keep the change focused, read the import requirements and existing tests, then implement and verify each required transition.

The importer has no state yet. I’ll add a per-instance busy set and use `finally` to clear only the active key. The regression tests will cover duplicates in both phases, independent work, failures, cancellation, and retries while leaving the two existing tests unchanged.

All six tests passed, including both original tests. The new tests cover the required failure and cancellation transitions and check that another key remains active. I’m checking the final diff and confirming the original test file is unchanged.

Implemented per-instance `busy_keys` and same-key duplicate suppression in `importer.py`, with cleanup on success, failure, and cancellation.

Preserved both existing tests unchanged and added native regression coverage for every specified transition.

Validation: `python3 -B -m unittest discover -v` — all 6 tests passed.
