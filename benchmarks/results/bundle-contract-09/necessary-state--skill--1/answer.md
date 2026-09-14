I’ll use the hostage-negotiator skill to keep the change focused, preserve existing save behavior, and add the required regression checks.


The UI already uses `Form.pending` to disable Submit. I’ll add per-instance state, suppress duplicate saves while pending, and clear the state in `finally` so success, failure, and cancellation all release the button. There’s no existing test suite or runner configuration, so I’ll use Python’s standard-library `unittest`.


Implemented per-instance `Form.pending`: Submit disables during save and re-enables after success, failure, or cancellation. Overlapping submissions cannot invoke another save.

All 6 retained regression tests passed, covering requested states, isolation, value/error identity, retries, and cancellation. Async waits are bounded and owned tasks cleaned up. Unrelated files preserved.

Rerun: `python3 -m unittest discover -s tests -v`
