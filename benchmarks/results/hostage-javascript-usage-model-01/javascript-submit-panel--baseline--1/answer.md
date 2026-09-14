I’ll read the requirements and existing tests, implement `pending`, and add native regression tests without changing the two existing tests.

The implementation now sets `pending` before invoking save, suppresses overlapping submissions, and clears it in `finally`. The regression tests use controlled promises, immediate rejection handlers, bounded waits, and cleanup that settles callbacks and drains tasks even if an assertion fails. I’ll run the suite now.

Implemented `SubmitPanel.pending` with per-instance duplicate suppression and cleanup after success or failure, preserving the existing API and identity behavior.

Added four rerunnable regression tests covering all requested scenarios, with bounded waits and callback/task cleanup. Both existing tests remain unchanged.

Verification: `node --test` passed all 6 tests; `git diff --check` passed.
