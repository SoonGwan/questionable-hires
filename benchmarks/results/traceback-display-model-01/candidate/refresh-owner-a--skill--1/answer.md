I’ll read the requested skill and requirements, review `Preview.refresh`, and add controlled-callback tests. I’ll change `preview.py` only if the review or tests show a mismatch.


`refresh` currently clears `pending` whenever any call settles, so an earlier call can clear it while the latest is still loading. I’m applying the requested hostage-negotiator skill to keep the fix focused and using its controlled-callback helper for bounded waits and task cleanup.


The first native run reported 5 tests with 6 failures, exit 1. Each failure shows an earlier call clearing `pending` while the latest call or retry remains unresolved. I’ll guard that cleanup with the existing generation check, then rerun the suite.


Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Native `python3 -B -m unittest discover -v` results:
- Before fix: 5 tests, 6 failures; exit 1.
- After fix: 5 tests, **OK**; exit 0.
