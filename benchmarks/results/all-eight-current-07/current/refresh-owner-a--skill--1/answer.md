I’ll use the hostage-negotiator skill to keep the review focused, check `Preview.refresh` against the requirements, and run the requested unittest command after adding coverage.

`Preview.refresh` clears `pending` whenever any call settles, so an earlier call can incorrectly clear it while the latest call is still running. I’ll guard that cleanup with the existing generation check and add controlled-callback tests for ownership, failures, cancellation, retry, and instance isolation.

All seven tests passed, including both latest-failure and latest-cancellation retry cases; the test process exited with code 0. I’ll check the final diff to confirm the changes are limited to the fix and tests.

Fixed `Preview.refresh` so only the latest-started call clears `pending`, preserving overlapping calls.

Added standard-library tests covering the requested completion, failure, cancellation, retry, identity, retention, and isolation cases, with bounded waits, task cleanup, and no timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests ran, all OK; process exit 0**.

Requirements and owner notes remain unchanged.
