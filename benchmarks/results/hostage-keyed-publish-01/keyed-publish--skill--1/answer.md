I’ll use the hostage-negotiator skill to keep the change focused on Publisher and the required regressions. I’ll read the project requirements, implementation, and test setup first.

Publisher currently forwards every call directly to `write`. I’ll add an instance-owned set of pending document IDs and clear each entry in `finally`, covering success, failure, and cancellation. The regressions will hold writes pending while checking suppression and concurrency, with bounded waits and task cleanup.

Implemented per-instance duplicate suppression with cleanup after success, failure, and cancellation. Preserved the callback contract and unrelated files.

`python3 -B -m unittest discover -s tests -v` passed all 9 tests: 2 unchanged existing tests and 7 new bounded regressions with owned-task cleanup.

`git diff --check` passed.
