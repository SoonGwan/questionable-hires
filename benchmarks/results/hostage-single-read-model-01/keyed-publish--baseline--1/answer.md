I’ll read `requirements.md` and the Publisher, add pending-write suppression and regression tests, then run both the existing and new tests.

All 9 tests passed, including the 2 existing tests and 7 new regressions. The Publisher now tracks pending document IDs per instance and clears them in `finally`. I’ll check the diff to confirm unrelated files and existing tests are unchanged.

Implemented per-instance pending-document suppression with cleanup after success, failure, or cancellation, preserving the write callback contract.

Added 7 bounded regression tests with owned-task cleanup. Existing tests and unrelated files remain unchanged.

Observed verification:
- `python3 -B -m unittest discover -s tests -v`: all 9 tests passed.
- `git diff --check`: passed.
