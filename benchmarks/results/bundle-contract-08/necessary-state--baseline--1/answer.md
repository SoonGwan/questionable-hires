I’ll inspect the save flow, add pending state, and retain regression tests for the requested success, failure, overlap, and cancellation cases.

The UI uses `Form.pending` to disable Submit. I’ll add that state per instance, ignore duplicate submissions while pending, and clear it in `finally` so success, failure, and cancellation all re-enable Submit. The tests will use the standard library with bounded waits and task cleanup.

Implemented per-instance `Form.pending`: Submit stays disabled during save, overlapping duplicates are ignored, and success, failure, or cancellation clears pending.

Added six rerunnable regression tests covering all requested behaviors, with bounded waits and owned-task cleanup. All pass:

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`

Unrelated files were preserved.
