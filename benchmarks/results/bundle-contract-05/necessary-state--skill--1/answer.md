I’ll use the hostage-negotiator skill to keep this focused on pending state and the required regression checks. I’ll inspect the project’s save flow and test setup first.


The UI reads `Form.pending`, and duplicate submissions must skip `save`. I’ll add per-instance state and clear it in `finally` so success, failure, and cancellation all re-enable Submit. I’ll use standard-library tests; the project has no existing test setup or dependencies.


Implemented per-instance `Form.pending`: Submit disables during save, overlapping submissions skip save, and success, failure, or cancellation clears pending.

Added 7 rerunnable regression tests covering all requested behavior, including value/error identity and retries. Async waits are bounded; owned tasks are cleaned up.

Verified: `python3 -B -m unittest -v` passes all 7 tests; diff checks pass. Unrelated files and existing user changes were preserved.
