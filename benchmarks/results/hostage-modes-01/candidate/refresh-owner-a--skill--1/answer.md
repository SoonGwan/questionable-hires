I’m using the hostage-negotiator skill to review `Preview.refresh`, keep any fix focused, and add controlled async tests with native unittest results.



`refresh` already guards value publication, but its unconditional `finally` lets an earlier call clear `pending` while the latest call is still running. I’ll apply the same ownership check to cleanup and test overlapping calls in both completion orders, including failures, cancellation, and retry.



The first run had six passing tests and two errors in the cancellation tests. The test helper shadowed `unittest.TestCase.fail`, and Python 3.9 did not preserve cancellation exception identity across the task boundary. I’ll fix the helper, check cancellation propagation, and retain exact identity assertions for fetched results and ordinary errors.



Fixed `Preview.refresh` so only the latest-started call clears `pending`; overlapping calls remain allowed.

Added eight standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes were preserved.

Final native run: `python3 -B -m unittest discover -v` — **8 tests, all OK; process exit 0**. `git diff --check` also passed.
