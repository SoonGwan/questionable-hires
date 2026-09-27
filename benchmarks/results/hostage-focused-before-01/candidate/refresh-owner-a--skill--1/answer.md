I’ll use the requested hostage-negotiator skill, check `Preview.refresh` against `requirements.md`, and add controlled concurrency tests before running the specified unittest command.

`refresh` already protects value publication, but its unconditional `finally` lets an earlier call clear `pending` while the latest call is still running. I’ll add a regression test for that failure, cover the other requested transitions, and apply the same ownership check to pending cleanup.

The regression test failed as expected: completing the earlier call set `pending` to `False` while the latest call remained unresolved. That test process exited with code 1. I’ll now guard pending cleanup with the existing generation check and run the full suite.

Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Native results:
- Before fix: targeted regression failed; exit **1**.
- After fix: `python3 -B -m unittest discover -v` ran **8 tests**, all **OK**; exit **0**.
