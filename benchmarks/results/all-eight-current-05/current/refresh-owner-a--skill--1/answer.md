I’ll use the hostage-negotiator skill to review the refresh behavior, make any required fix, and add bounded unittest coverage within this project.

`refresh` always clears `pending` in its `finally` block, so an earlier call can clear it while the latest call is still waiting. I’ll cover that ownership bug and the required recovery paths with controlled callbacks, then guard cleanup using the existing generation check.

Fixed `Preview.refresh` so only the latest-started call clears `pending`; overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps.

Actual `python3 -B -m unittest discover -v` results:
- Before fix: 8 tests, 5 failures; exit 1.
- After fix: 8 tests, all OK; exit 0.

Requirements and owner notes are unchanged. Diff and helper integrity checks passed.
