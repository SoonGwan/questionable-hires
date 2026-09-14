I’ll compare `Preview.refresh` with the requirements, add controlled async tests, and run the requested unittest command to verify the results and exit code.

`refresh` clears `pending` unconditionally, so an older call can clear it while the latest call is still waiting. I’ll make that cleanup conditional on ownership and use futures to test completion order, failures, and cancellation without timing sleeps.

Fixed `preview.py` so only the latest-started refresh clears `pending`; overlapping calls remain independent.

Added 7 standard-library tests covering all requested scenarios, with controlled callbacks, bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual `python3 -B -m unittest discover -v` results:
- Before fix: `FAILED (failures=7)`, exit 1.
- After fix: `Ran 7 tests in 0.054s` — `OK`, exit 0.
