I’ll check `Preview.refresh` against the requirements, add controlled overlap tests, and run the requested unittest command.


The `finally` block clears `pending` unconditionally, so an earlier call can clear it while the latest call is still unresolved. I’ll add tests that control callback completion directly, then guard that cleanup by generation.


The first run exited 1 with six failures: five expose the pending-state bug. The sixth is a test issue—Python 3.9 replaces the cancellation exception at the task boundary. I’ll check its identity directly at the `refresh` boundary and apply the generation guard.


Fixed `preview.py` so only the latest-started refresh clears `pending`; overlapping calls remain independent.

Added six standard-library unittest tests covering all requested scenarios, with controlled callbacks, bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual native run of `python3 -B -m unittest discover -v`:

```text
Ran 6 tests in 0.037s

OK
```

Test process exit: **0**.
