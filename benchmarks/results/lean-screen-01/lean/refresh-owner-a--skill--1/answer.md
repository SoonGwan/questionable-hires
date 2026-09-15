I’ll use the hostage-negotiator skill to check `Preview.refresh` against the requirements, make any necessary fix, and add controlled async tests within this project.

`Preview.refresh` has one ownership bug: every call clears `pending` when it settles, including an older call while the latest is still running. I’ll add the tests first, then guard that cleanup with the existing generation check.

Fixed `preview.py` so only the latest-started refresh clears `pending`; overlapping calls remain allowed.

Added controlled standard-library tests covering all requested cases, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Native `python3 -B -m unittest discover -v` results:
- Before fix: 6 failures; exit 1.
- After fix: 5 tests ran, `OK`; exit 0.
