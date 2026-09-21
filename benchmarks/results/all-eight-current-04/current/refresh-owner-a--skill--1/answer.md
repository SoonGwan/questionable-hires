I’ll use the requested hostage-negotiator skill, review `Preview.refresh` against the requirements, and add controlled-callback tests before running the specified unittest command.

`Preview.refresh` clears `pending` whenever any call settles, so an earlier call can clear it while the latest is still waiting. I’ll add tests for that ownership bug and the other required transitions, then guard cleanup with the existing generation check.

The baseline run reported 7 tests with 5 failures (exit 1), all showing an earlier call clearing `pending` while the latest remained unresolved. I’ll apply the generation guard and rerun the same command.

Fixed `preview.py` so only the latest-started refresh clears `pending`; overlapping callbacks remain independent.

Added 7 standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual `python3 -B -m unittest discover -v` results:
- Before fix: 7 tests, 5 failures; exit 1.
- After fix: 7 tests, `OK`; exit 0.

`git diff --check` also passed.
