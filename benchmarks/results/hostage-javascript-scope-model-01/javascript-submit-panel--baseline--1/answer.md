I’ll read the project requirements and existing tests, implement `pending`, and add native regression tests with bounded waits and cleanup.


The requirements call for an instance-level guard set before `save` runs and cleared in `finally`. I’ll leave both existing tests unchanged and add a separate test file that settles controlled callbacks and drains submission tasks even if an assertion fails.


Implemented `SubmitPanel.pending` with per-instance duplicate suppression and cleanup after success or failure, preserving the existing API.

Added five regression tests covering all requested scenarios, with bounded waits, prompt rejection handling, and callback/task cleanup. Both existing tests remain unchanged.

Verification: `node --test` passes all 7 tests; `git diff --check` passes.
