I’ll use the hostage-negotiator skill to review `Preview.refresh`, make any required fix, and add controlled async tests within this project.


`Preview.refresh` always clears `pending` in `finally`, so an earlier call can clear it while the latest call is still unresolved. I’ll guard that cleanup by the existing generation check and test overlapping calls, settlement, and recovery.


The native run reproduced the bug: 4 of 9 tests failed, with exit code 1. Earlier success, failure, and cancellation cleared `pending`; an older completion also cleared it during a retry. I’ll apply the ownership guard and rerun the suite.


Fixed `Preview.refresh` so only the latest-started call clears `pending`, preserving overlapping execution.

Added 9 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps.

Actual native results for `python3 -B -m unittest discover -v`:
- Before fix: 9 tests, 4 failures; exit 1.
- After fix: 9 tests, all OK; exit 0.

Requirements and owner notes remain unchanged. Helper integrity and diff checks passed.
