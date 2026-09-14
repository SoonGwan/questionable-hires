I’ll inspect the save flow and test setup, add pending state, and verify duplicate prevention and cleanup across success, failure, and cancellation.


The UI reads `Form.pending`, and duplicate submissions must leave the active save alone. I’ll add per-instance pending state and clear it in `finally` so success, failure, and cancellation all re-enable Submit. Regression tests will use bounded waits and clean up their tasks.

