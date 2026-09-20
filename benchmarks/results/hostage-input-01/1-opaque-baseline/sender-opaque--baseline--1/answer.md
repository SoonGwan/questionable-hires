I’ll read the sender contract and existing tests, make the focused fix, and run the documented unittest suite.

The sender clears `pending` only after successful delivery. A `finally` block will clear it on failure and cancellation too, while preserving results, exceptions, and payload identity. I’ll add regressions for those paths, retries, duplicate suppression, and independent instances, with bounded waits and task cleanup.

Fixed `Sender.send` with `try/finally` so every settlement clears `pending`, preserving payload identity, results, and errors.

Extended `test_sender.py` while retaining existing assertions. Coverage includes failures, cancellation, retries, duplicate suppression, independent instances, and opaque payload identity. Owned tasks are cleaned up in `finally`.

Validation: three regressions failed before the fix; all 6 tests passed afterward using `python3 -B -m unittest discover -v`. `git diff --check` passed.

Limitations: tested on the available Python 3.9 runtime with cooperative callbacks only. Only the two requested files changed.
