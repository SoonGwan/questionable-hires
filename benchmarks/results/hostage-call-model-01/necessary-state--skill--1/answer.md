I’ll use the hostage-negotiator skill to keep the change focused, inspect the save owner and existing tests, and add the required regression checks.


The UI already uses `Form.pending` to disable Submit, so the change belongs in `Form.submit`: set pending before calling save, ignore overlapping submissions, and clear it in `finally`. There’s no existing test runner; I’ll use Python’s standard-library `unittest` with bounded async waits and task cleanup.


Implemented `Form.pending` to disable Submit during saving, suppress overlapping submissions, and reset after success, failure, or cancellation.

All 6 regression tests pass, covering required states, instance independence, value/error identity, retries, and cancellation. Async waits are bounded and owned tasks cleaned up. Unrelated files were preserved.

Rerun: `python3 -m unittest discover -v`
