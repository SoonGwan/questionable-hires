I’ll inspect the save flow, add pending-state protection, and retain regression tests for the requested success, failure, overlap, and cleanup cases.

The UI uses `Form.pending` to disable Submit. I’ll add an instance-level flag, ignore duplicate submissions while it’s set, and clear it in `finally` so success, failure, and cancellation all re-enable Submit.

Implemented `Form.pending` with duplicate submission prevention and cleanup after success, failure, or cancellation.

Added 5 passing regression tests covering all requested cases, with bounded waits and owned-task cleanup. Unrelated files preserved.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`
