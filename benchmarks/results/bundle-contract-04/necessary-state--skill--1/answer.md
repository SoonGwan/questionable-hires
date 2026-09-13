I’ll use the hostage-negotiator skill to keep this focused, inspect the save owner, and add bounded regression tests for the required state and cleanup behavior.

The UI already reads `Form.pending` to disable Submit. I’ll add per-instance state, ignore duplicate submissions while pending, and clear the state in `finally` so success, failure, and cancellation all re-enable Submit. The project has no test suite, so I’ll add tests using Python’s standard library.

Implemented per-instance `pending` state, duplicate submission prevention, and cleanup after success, failure, or cancellation.

All 6 regression tests pass, covering the required transitions, instance independence, return/exception identity, and retries. Tests use bounded waits and clean up owned tasks.

Rerun: `python3 -B -m unittest -v`

Unrelated files and existing user changes were preserved.
