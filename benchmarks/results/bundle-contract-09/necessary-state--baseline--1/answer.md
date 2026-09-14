I’ll inspect the save flow and test setup, add pending-state handling, and verify the requested cases with rerunnable tests.


The UI reads `Form.pending`, and overlapping submissions must skip the save call. I’ll add per-instance state and clear it in `finally` so success, failure, and cancellation all re-enable Submit. Tests will use controlled events, bounded waits, and task cleanup.


Implemented per-instance `Form.pending`: it starts false, blocks duplicate saves while true, and resets after success, failure, or cancellation.

Added 7 passing regression tests covering all requested cases, with bounded waits and owned-task cleanup. Unrelated files remain unchanged.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`
