I’ll compare `Preview.refresh` with the requirements, add controlled async tests, and run the requested unittest command to verify the results and exit code.

`Preview.refresh` already meets the requirements: its generation check gives the latest call control of `pending` and `value`, and `finally` handles synchronous failures and cancellation. I’ll leave `preview.py` unchanged and add tests that control callback completion without timing sleeps.

The first run failed three cancellation assertions. This environment’s Python 3.9 `Task.result()` returns a fresh `CancelledError`, losing the original identity and message. I’ll capture exceptions directly at the `refresh` boundary so those assertions test `Preview`’s behavior rather than the task wrapper.

`Preview.refresh` meets the requirements; `preview.py` remains unchanged.

Added `test_preview.py` covering all requested scenarios with controlled callbacks, bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are preserved.

Native verification: `python3 -B -m unittest discover -v`
- Ran 6 tests in 0.031s
- Result: `OK`
- Process exit: `0`
