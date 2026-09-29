I’ll review `Preview.refresh` against the requirements, add controlled-callback tests, and run the requested unittest command. I’ll change `preview.py` only if the review exposes a mismatch.

`refresh` clears `pending` unconditionally, so an earlier call can clear it while the latest call is still unresolved. I’ll make that cleanup conditional on ownership and add tests for overlapping calls, failures, cancellation, retries, and retained display values.

All eight tests passed, and the test process exited with code 0. The tests use callback signals and controlled futures, bound their waits, and clean up owned refresh tasks without timing sleeps. I’ll check the final diff for unrelated changes.

Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added eight standard-library tests covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual run: `python3 -B -m unittest discover -v`
- Ran 8 tests in 0.035s
- Result: `OK`
- Process exit: `0`
