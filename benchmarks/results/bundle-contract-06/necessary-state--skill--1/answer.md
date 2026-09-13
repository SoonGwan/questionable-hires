I’ll use the hostage-negotiator skill to keep this focused on Submit’s pending state and the required regression checks. I’ll inspect the project, implement the change, and verify cleanup and retry behavior without touching unrelated files.


The UI already reads `Form.pending`, and the requirements say duplicate submissions must not invoke save again. I’ll add per-instance state and clear it in `finally` so success, failure, and cancellation all re-enable Submit. The project has no tests, so I’ll add rerunnable tests using Python’s standard library.


Implemented per-instance `Form.pending` to disable Submit during save and clear it on success, failure, or cancellation. Overlapping submissions skip save; return values and exceptions retain identity.

All six regression tests pass, covering every requested behavior with bounded waits and task cleanup.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`

Unrelated files and existing user changes were preserved.
