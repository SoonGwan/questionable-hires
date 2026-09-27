I’ll use the hostage-negotiator skill to keep the review focused, check `Preview.refresh` against the requirements, and add and run the requested unittest coverage.

`refresh` clears `pending` whenever any call settles. That violates the requirement when an earlier call finishes while the latest is still pending. I’ll add controlled-callback tests for the requested transitions, then guard that cleanup with the existing generation check.

Fixed `preview.py` so only the latest-started refresh clears `pending`; overlapping callbacks remain independent.

Added standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes were preserved.

Actual native results from `python3 -B -m unittest discover -v`:

- Before fix: 5 tests, 5 subtest failures; exit **1**.
- After fix: 5 tests, **OK**; exit **0**.

`git diff --check` also passed.
