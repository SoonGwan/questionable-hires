I’ll use the hostage-negotiator skill to review the refresh contract, preserve owner changes, and add controlled async tests before deciding whether `preview.py` needs a fix.

`refresh` already invokes overlapping callbacks and guards value publication, but its unconditional `finally` lets an earlier call clear `pending` while the latest is still running. I’ll add tests to demonstrate that failure, then guard pending cleanup by the same ownership check.

Fixed `Preview.refresh` so only the latest-started call clears `pending`. Overlapping callbacks remain concurrent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 8 tests, 5 failures; process exit **1**.
- After fix: 8 tests, **OK**; process exit **0**.

Requirements and owner notes are unchanged. Diff and helper-integrity checks passed.
