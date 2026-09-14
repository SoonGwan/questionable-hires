I’m using the hostage-negotiator skill to keep this focused on pending state, duplicate prevention, and save cleanup. I’ll inspect the project and its test runner, implement the behavior, and retain regression tests for the required cases.

The UI contract reads `Form.pending`, so each instance needs a pending flag and a duplicate guard. I’ll clear the flag in `finally` to cover success, failure, and cancellation. The project has no test runner configured; I’ll use standard-library `unittest` with the skill’s controlled callback helper.

Implemented per-instance `Form.pending`, duplicate submission suppression, and cleanup on success, failure, or cancellation.

Six retained regression tests pass, covering all requested cases, with bounded waits and owned-task cleanup. Return and exception identity are preserved. Unrelated files remain unchanged.

Rerun: `python3 -m unittest discover -v`
