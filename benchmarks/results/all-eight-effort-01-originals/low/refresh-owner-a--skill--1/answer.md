I’ll use the hostage-negotiator skill to review the refresh contract, keep changes focused, and add controlled async tests before running the requested unittest command.


`refresh` already limits publishing to the latest call, but every call clears `pending` in `finally`. That violates the requirement when an earlier call settles while the latest is still pending. I’ll add regression coverage, then apply the same ownership check to cleanup.


Fixed `Preview.refresh` so only the latest-started call clears `pending`; overlapping calls remain independent.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Native `python3 -B -m unittest discover -v` results:
- Before fix: 8 tests, 4 failures; exit 1.
- After fix: 8 tests, all OK; exit 0.

Diff and helper-integrity checks also passed.
