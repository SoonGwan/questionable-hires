I’ll read the requirements and `Preview.refresh`, add controlled-callback tests, and fix `preview.py` if needed. Then I’ll run the requested unittest command and report its output and exit code.


`refresh` has an ownership bug: every call clears `pending` in `finally`, so an earlier call can clear it while the latest is still waiting. I’ll guard that assignment with the existing generation check and test the overlapping calls in both completion orders.


Fixed `preview.py` so only the latest-started refresh clears `pending`.

Added 7 standard-library unittest tests covering all requested scenarios, using actual `Preview`, controlled callbacks, bounded waits, task cleanup, and no timing sleeps.

Actual run: `python3 -B -m unittest discover -v`
- Ran 7 tests in 0.052s
- Result: `OK`
- Process exit: `0`

Requirements and owner notes remain unchanged.
