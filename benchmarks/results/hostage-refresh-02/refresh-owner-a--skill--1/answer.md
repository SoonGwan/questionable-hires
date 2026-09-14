I’ll use the hostage-negotiator skill to review `Preview.refresh`, keep any fix focused, and add controlled async tests. I’ll run the requested unittest command and report its native results and exit code.


`Preview.refresh` clears `pending` unconditionally, so an earlier call can clear it while the latest call is still waiting. I’ll test that ownership rule across success, failure, cancellation, and retry, then guard the cleanup with the existing generation check.


Fixed `preview.py` so only the latest-started refresh clears `pending`; overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 8 tests, 5 failures; exit 1.
- After fix: 8 tests in 0.047s, `OK`; exit 0.
