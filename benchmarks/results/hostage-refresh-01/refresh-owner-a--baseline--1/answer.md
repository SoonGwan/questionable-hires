I’ll compare `Preview.refresh` with the requirements, fix it if needed, and add controlled concurrency tests. Then I’ll run the requested unittest command and report its output and exit code.

`Preview.refresh` has one mismatch: every call clears `pending` when it settles, including older calls while the latest is unresolved. I’ll guard that cleanup with the existing generation check and test overlapping calls using explicitly controlled futures.

The first run exited with code 1, with five cancellation assertions failing. This native runtime exposes a fresh `CancelledError` through `Task.result()`, so I’ll capture exceptions as they leave `Preview.refresh` to test identity at that boundary, while still checking task cancellation separately.

Fixed `preview.py`: only the latest refresh now clears `pending`. Overlapping calls remain independent.

Added `test_preview.py` covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Ran `python3 -B -m unittest discover -v` twice after correcting the cancellation test harness. Both native runs reported:

```text
Ran 5 tests in 0.041s

OK
```

Both test processes exited with code **0**.
