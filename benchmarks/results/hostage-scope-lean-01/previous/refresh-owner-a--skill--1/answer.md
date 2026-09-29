I’ll read the hostage-negotiator skill and requirements, review `Preview.refresh`, then add controlled-callback tests and run the requested unittest command.

`Preview.refresh` clears `pending` whenever any call settles, so an earlier call can clear it while the latest is still pending. I’ll add tests for that ownership bug and the requested recovery cases, then guard cleanup with the existing generation check.

Fixed `Preview.refresh` so only the latest-started call clears `pending`; overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual native results from `python3 -B -m unittest discover -v`:

- Before fix: 8 tests, 5 failures; process exit **1**.
- After fix: 8 tests in 0.035s, **OK**; process exit **0**.
