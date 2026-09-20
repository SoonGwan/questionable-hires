I’ll compare `Preview.refresh` with the requirements, add controlled-callback tests, and run the requested unittest command. I’ll change `preview.py` only if the review finds a defect.

The `finally` block clears `pending` unconditionally, so an older call can clear it while the latest call is still loading. Value publication already checks which call owns it. I’ll add tests using futures to control completion order, then apply the same ownership check to `pending`.

The first run reproduced four failures, all from older calls clearing `pending` while the latest remained unresolved; the process exited with code 1. I’ll now add the ownership guard. The tests use bounded waits and task cleanup, with no timing sleeps.

Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain unrestricted.

Added `test_preview.py` covering all requested scenarios using actual `Preview`, controlled callbacks, bounded waits, and task cleanup—without timing sleeps.

Actual native run of `python3 -B -m unittest discover -v`:

```text
Ran 5 tests in 0.036s

OK
```

Test process exit: **0**. Before the fix: four failures, exit **1**.

Requirements and owner notes remain unchanged.
