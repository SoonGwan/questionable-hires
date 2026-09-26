I’ll use the hostage-negotiator skill to check `Preview.refresh` against the requirements, add controlled async tests, and change `preview.py` only if the review shows a mismatch.

The tests confirmed that an earlier refresh clears `pending` while the latest is still waiting. Five of eight tests failed on that condition. I’ll guard the `finally` block with the existing generation check so only the latest refresh can clear `pending`.

Fixed `Preview.refresh` so only the latest refresh clears `pending`; overlapping calls remain independent.

Added eight standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Actual native results from `python3 -B -m unittest discover -v`:

- Before fix: 8 tests, 5 failures; process exit **1**.
- After fix: 8 tests, **OK**; process exit **0**.

Diff checks and helper copy integrity passed.
