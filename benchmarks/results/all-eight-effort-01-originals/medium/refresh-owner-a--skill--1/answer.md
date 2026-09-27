I’ll use the hostage-negotiator skill to review the refresh contract, keep any fix focused, and verify it with controlled async unittest tests.



`refresh` already limits publishing to the latest call, but every call clears `pending` when it settles. An earlier call can therefore clear it while the latest is still running. I’ll add regression tests, then apply the same ownership check to cleanup.



Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 8 tests, 5 failures; exit 1.
- After fix: 8 tests, all OK; exit 0.

Diff checks and test-helper copy integrity passed.
