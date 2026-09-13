I’ll inspect the project, add pending-state handling around save, and retain regression tests for the requested success, failure, duplicate, and cancellation behavior.

The UI already expects `Form.pending`. I’ll add it per instance, ignore duplicate submissions while a save is pending, and clear it in `finally` so success, failure, and cancellation all re-enable Submit. I’ll use standard-library tests with bounded waits and task cleanup.

Implemented per-instance `Form.pending`: Submit disables during save and re-enables after success, failure, or cancellation. Overlapping submissions skip save; return values and exceptions preserve identity.

Added six passing regression tests covering all requested behaviors, with bounded waits and owned-task cleanup. Unrelated files preserved.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`
