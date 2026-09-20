I’ll use the hostage-negotiator skill to check `Preview.refresh` against the requirements, make any needed fix, and add controlled async tests within this project.

`Preview.refresh` clears `pending` unconditionally, so an earlier call can clear it while the latest call is still unresolved. I’ll guard that cleanup with the existing generation check and test the requested completion, failure, cancellation, and retry cases.

Fixed `Preview.refresh` so only the latest-started call clears `pending`, preserving overlapping calls.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual native result from `python3 -B -m unittest discover -v`: **8 tests ran, all OK; process exit 0**. Helper integrity and diff checks also passed.
