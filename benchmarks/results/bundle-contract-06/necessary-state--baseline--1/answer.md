I’ll inspect the save flow and existing tests, add pending-state handling, and verify the requested cases with rerunnable tests.


The UI reads `Form.pending`, and duplicate submissions must skip `save`. I’ll add per-instance pending state and clear it in `finally` so success, failure, and cancellation all re-enable Submit. The tests will use bounded waits and clean up every task they create.


Implemented per-instance `Form.pending`, duplicate submission prevention, and cleanup after success, failure, or cancellation.

Added 7 passing regression tests covering all requested cases, with bounded waits and owned-task cleanup. Unrelated files remain unchanged.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`
