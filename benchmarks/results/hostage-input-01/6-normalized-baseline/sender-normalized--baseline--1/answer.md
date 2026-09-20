I’ll read the sender contract and existing tests, make a focused fix, and run the documented unittest suite.

The contract requires payload normalization and the original result or error to be preserved. I’ll put delivery inside `try/finally` so every settlement clears `pending`, then add regressions for failures, cancellation, retries, duplicates, independent instances, and normalized callback arguments.

Fixed `Sender.send` with `try/finally` so failure and cancellation clear `pending`, preserving normalization, duplicate suppression, results, and errors.

Retained existing assertions and added six regressions covering cleanup, retries, duplicates, independent instances, and padded mixed-case Unicode callback inputs.

`python3 -B -m unittest discover -v`: **7 tests passed**. `git diff --check` passed.

Only `sender.py` and `test_sender.py` changed. Validation covers cooperative local callbacks; no external services were used.
