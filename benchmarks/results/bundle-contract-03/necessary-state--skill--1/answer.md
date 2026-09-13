I’ll use the hostage-negotiator skill to keep the change focused, inspect the save flow, and add rerunnable checks for the required state and cleanup behavior.

The UI reads `Form.pending`, and overlapping submissions must not call save again. I’ll add per-instance state with `finally` cleanup and use standard-library tests with bounded waits.

Implemented per-instance `Form.pending`: Submit disables during save and re-enables after success, failure, or cancellation. Overlapping submissions skip save; return values and exceptions retain identity.

All 7 regression tests pass, covering every requested scenario with bounded waits and task cleanup. Unrelated files and existing changes were preserved.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`
