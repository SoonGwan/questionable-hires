I’ll use the hostage-negotiator skill to review `Preview.refresh`, add controlled async tests, and change `preview.py` only where the requirements call for it.

`refresh` clears `pending` unconditionally in `finally`, so an earlier call can clear it while the latest call is still waiting. I’ll guard that cleanup with the existing generation check and test overlapping calls, failures, cancellation, and recovery.

All 8 tests passed in the native unittest run, with process exit 0. They cover the requested overlap and recovery cases using controlled callbacks, bounded waits, and task cleanup. I’m checking the final diff and helper copy for scope and integrity.

Fixed `Preview.refresh` so only the latest-started call clears `pending`, preserving overlapping execution.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Verification: `python3 -B -m unittest discover -v` reported **8 tests, all OK**, process exit **0**. Helper integrity and diff checks also passed.
