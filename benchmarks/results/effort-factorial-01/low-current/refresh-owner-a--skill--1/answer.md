I’ll use the hostage-negotiator skill, review `Preview.refresh` against the requirements, and add controlled concurrency tests before running the requested unittest command.


`refresh` already guards value publication, but its unconditional `finally` lets an older call clear `pending` while the latest call is still unresolved. I’ll cover that bug and the requested settlement and retry cases, then add the same ownership guard to pending-state cleanup.


Fixed `preview.py` so only the latest-started refresh clears `pending`. Overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual native results for `python3 -B -m unittest discover -v`:

- Before fix: 8 tests, 5 failures; process exit **1**.
- After fix: 8 tests, **OK**; process exit **0**.
