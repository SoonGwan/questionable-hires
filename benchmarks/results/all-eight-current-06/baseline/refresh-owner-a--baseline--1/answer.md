I’ll compare `Preview.refresh` with the requirements, add controlled-callback tests, and run the requested unittest command.

`Preview.refresh` has an ownership bug: every call clears `pending` in `finally`, so an earlier call can clear it while the latest is still unresolved. I’ll guard that cleanup with the existing generation check and test each completion order using futures and events, without timing sleeps.

Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added rerunnable standard-library tests covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual run: `python3 -B -m unittest discover -v`
- Ran 5 tests, including scenario subtests, in 0.037s
- Result: `OK`
- Process exit: `0`
