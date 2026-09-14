I’ll use the hostage-negotiator skill to keep the change focused, read the requirements and existing tests, then implement and verify the specified transitions with the project’s native runner.

The requirements fit a per-instance busy set: claim the key before fetch and release it in `finally`. I’ll add controlled async tests for duplicate suppression, independent imports, and recovery after failures or cancellation in either phase, while leaving the original tests unchanged.

Implemented per-instance `busy_keys` and same-key duplicate suppression in `importer.py`. Keys remain busy through fetch and persist, with cleanup on success, failure, or cancellation.

Both original tests are unchanged. Added eight regression tests covering required transitions, identities, retries, and independent keys/instances.

All 10 tests pass with `python3 -B -m unittest discover -v`.
