I’ll use the hostage-negotiator skill to review the refresh lifecycle, add controlled async regression tests, and change `preview.py` only where the requirements demand it.

`refresh` already guards value publication, but its unconditional `finally` lets an earlier call clear `pending` while the latest call is still running. I’ll add tests that reproduce this and check recovery, identity, display retention, and instance isolation.

The initial run reproduced the bug: 5 of 8 tests failed because an older call cleared `pending`, including during a retry. I’ll guard the `finally` cleanup with the existing generation check so only the latest call clears it.

Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 8 tests, 5 failures; exit **1**.
- After fix: 8 tests, **OK**; exit **0**.
