I’ll inspect the save flow and existing tests, add pending-state handling, and verify the requested edge cases with rerunnable tests.


The UI already expects `Form.pending`, and duplicate submissions must skip the save call. I’ll add an instance-level flag and clear it in `finally` so success, failure, and cancellation all re-enable Submit. The regression tests will use events and bounded waits.


Implemented `Form.pending`: Submit disables during save and re-enables after success, failure, or cancellation. Overlapping submissions skip saving.

All 6 retained regression tests pass, covering state transitions, duplicates, independent instances, return/exception identity, failure/retry, and cancellation cleanup. Tests bound waits and clean up owned tasks. Unrelated files remain unchanged.

Rerun: `python3 -m unittest -v`
