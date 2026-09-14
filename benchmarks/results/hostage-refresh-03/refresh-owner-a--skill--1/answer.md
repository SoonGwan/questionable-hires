I’ll use the hostage-negotiator skill to review `Preview.refresh`, fix it only if needed, and add controlled async tests for the required transitions.

`refresh` already limits value updates to the latest call, but its unconditional `finally` lets an earlier call clear `pending`. I’ll add the same ownership check there and test overlapping calls with explicitly controlled completion, failure, and cancellation.

Fixed `Preview.refresh` so only the latest-started call clears `pending`; overlapping calls remain enabled.

Added controlled standard-library tests covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

`python3 -B -m unittest discover -v`: **7 tests ran, all OK. Process exit: 0.** Helper integrity and diff checks also passed.
