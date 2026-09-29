I’ll compare `Preview.refresh` with `requirements.md`, add controlled-callback tests, and run the requested unittest command.


`refresh` clears `pending` unconditionally, so an earlier call can clear it while the latest call is still waiting. I’ll make that cleanup conditional on ownership and test the overlapping calls with futures, using bounded waits and no timing sleeps.


Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added standard-library tests covering all requested scenarios with controlled callbacks, bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual run: `python3 -B -m unittest discover -v`

```text
Ran 5 tests in 0.030s

OK
```

Test process exit: `0`.
