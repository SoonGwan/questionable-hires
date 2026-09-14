I’ll use the hostage-negotiator skill to keep the change focused on Publisher, preserve its callback contract, and add bounded regression tests for pending writes and recovery.


Publisher currently forwards directly to the callback. I’ll add a per-instance set of pending document IDs and clear each entry in `finally`, covering success, failure, and cancellation. The new tests will hold writes open to check suppression and concurrency, using the skill’s controlled-call helper.


Implemented per-instance duplicate suppression with cleanup after success, failure, and cancellation. Preserved callback arguments, result/error identity, and concurrency for different documents and instances.

Added bounded regression tests with task cleanup. Existing tests remain unchanged.

Observed: `python3 -B -m unittest discover -s tests -v` passed all 7 tests. `git diff --check` passed.
