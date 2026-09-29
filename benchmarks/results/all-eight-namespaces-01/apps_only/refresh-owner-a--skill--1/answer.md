I’ll use the hostage-negotiator skill to review the refresh contract, add controlled async tests, and change `preview.py` only if the requirements call for it.

`Preview.refresh` clears `pending` whenever any call settles, so an earlier call can clear it while the latest is still waiting. I’ll add regression tests for that ownership bug and the required return, failure, cancellation, and retry behavior before applying the fix.

The initial run found five failures across eight tests (exit 1), all caused by an earlier completion clearing `pending` during a newer refresh. I’ll guard that cleanup with the existing generation check so only the latest call can clear it.

Fixed `preview.py`: only the latest-started refresh clears `pending`; overlapping calls remain independent.

Added eight standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 8 tests, 5 failures; exit 1.
- After fix: 8 tests in 0.035s, **OK**; exit 0.

Helper integrity and diff checks also passed.
