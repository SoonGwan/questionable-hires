I’m using the hostage-negotiator skill to keep the fix focused. I’ll read the contract and existing tests, update `Sender.send`, and run the documented unittest suite.



`send` only clears `pending` after a successful delivery. A `finally` block will cover errors and cancellation while preserving the exact callback argument, result, and error. I’ll add regressions with bounded waits and task cleanup so failures cannot leave the suite hanging.



Fixed `Sender.send` with `try/finally` so success, failure, and cancellation clear `pending`, preserving argument, result, and error identity.

Preserved existing assertions and added regressions for cleanup, duplicate suppression, retry, independent instances, and opaque payloads. Async tests use bounded waits and task cleanup.

`python3 -B -m unittest discover -v`: **7 tests passed**, exit 0.

Validation covers cooperative callbacks per the contract. Only `sender.py` and `test_sender.py` changed; unrelated files were preserved.
