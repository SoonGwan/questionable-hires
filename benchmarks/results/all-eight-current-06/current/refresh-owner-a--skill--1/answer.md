I’ll use the hostage-negotiator skill to keep the review focused, check `Preview.refresh` against the requirements, and add and run the requested unittest coverage.


`refresh` clears `pending` whenever any call settles. That violates the requirement when an earlier call finishes while the latest is still pending. I’ll add controlled-callback tests, confirm they catch this defect, then make the ownership check in `finally`.


Fixed `preview.py`: only the latest-started refresh can clear `pending`. Overlapping calls remain independent.

Added 10 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and unrelated notes were preserved.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 10 tests, 5 failures; process exit **1**.
- After fix: 10 tests, **OK**; process exit **0**.
