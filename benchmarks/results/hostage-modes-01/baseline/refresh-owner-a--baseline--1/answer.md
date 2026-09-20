I’ll compare `Preview.refresh` with the requirements, add controlled-callback tests, and run the requested unittest command.


`refresh` clears `pending` unconditionally, so an earlier call can clear it while the latest call is still loading. I’ll guard that cleanup by generation and test overlapping calls with explicit callback signals and bounded waits.


Fixed `preview.py` so only the latest-started refresh clears `pending`, preserving overlapping calls.

Added eight standard-library tests covering all requested scenarios, with controlled callbacks, bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual native run of `python3 -B -m unittest discover -v`:

```text
Ran 8 tests in 0.037s

OK
```

Test process exit: `0`.
