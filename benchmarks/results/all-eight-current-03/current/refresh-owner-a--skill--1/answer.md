I’ll use the hostage-negotiator skill to review `Preview.refresh`, add controlled async tests, and change `preview.py` only if the requirements reveal a gap. I’ll keep all work inside this project and report the native unittest results and exit code.



`Preview.refresh` clears `pending` unconditionally, so an earlier call can clear it while the latest call is still waiting. I’ll add regression tests for that ownership bug and the other requested transitions, then guard the cleanup by the existing generation check.



Before the fix, the native run reported five failures, all from earlier calls clearing `pending`. With the ownership guard added, all eight tests pass. I’m checking the final diff and confirming that requirements and owner notes remain untouched.



Fixed `preview.py` so only the latest-started refresh clears `pending`; overlapping calls remain independent.

Added eight standard-library tests using actual `Preview` and controlled callbacks, covering all requested scenarios with bounded waits, owned-task cleanup, and no timing sleeps.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 8 tests, 5 failures; exit **1**.
- After fix: 8 tests, **OK** in 0.047s; exit **0**.

Requirements and owner notes are unchanged. Diff checks and helper-copy integrity passed.
