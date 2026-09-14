I’ll use the hostage-negotiator skill to add pending-state handling and the required regression tests, keeping all work inside this project.

The UI already reads `Form.pending`, and duplicate submissions must skip `save`. I’ll add per-instance state with `finally` cleanup and use standard-library `unittest` for the regression tests; the project has no existing test runner or dependencies.

Implemented per-instance `Form.pending`: Submit disables during save and re-enables after success, failure, or cancellation. Overlapping submissions skip saving.

All 6 regression tests passed, covering required states, instance isolation, value/error identity, retry, and cancellation. Async waits are bounded and owned tasks cleaned up. Unrelated files preserved.

Rerun: `python3 -m unittest discover -v`
