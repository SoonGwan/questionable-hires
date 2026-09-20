I’ll use the hostage-negotiator skill to keep the fix focused, check the full sender contract, and add regressions in the existing unittest file.



The normalization already matches the contract. I’ll put delivery inside `try/finally` so success, failure, and cancellation all clear `pending`, then test retries, duplicate suppression, and instance independence with bounded waits and task cleanup.



Fixed `Sender.send` with `try/finally`, ensuring failure and cancellation clear `pending` while preserving normalization, result identity, and original errors.

Preserved existing assertions and added regressions for cleanup, duplicates, retries, independent instances, and Unicode normalization. Tests use bounded waits and owned-task cleanup.

`python3 -B -m unittest discover -v`: **6 tests passed**. `git diff --check` passed.

Validation covers cooperative asyncio callbacks within this synthetic project. Only `sender.py` and `test_sender.py` changed.
