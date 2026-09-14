I’ll inspect the save flow and tests, add pending-state handling, and verify cleanup and duplicate prevention within this project.

The UI already reads `Form.pending` to disable Submit. I’ll add that state per instance, ignore overlapping submissions, and clear it in `finally` so success, failure, and cancellation all re-enable Submit. The regression tests will use standard-library tools, bounded waits, and task cleanup.

Implemented per-instance `Form.pending`: overlapping submissions are ignored, and success, failure, or cancellation clears pending. Return values and exceptions retain their identity.

All 7 retained regression tests pass, covering the requested cases with bounded waits and owned-task cleanup. Unrelated files were preserved.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`
