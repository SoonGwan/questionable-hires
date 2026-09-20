I’m using the hostage-negotiator skill to keep this focused. I’ll read the contract, sender, tests, and working-tree status, then fix cleanup and run the documented suite.



`send` clears `pending` only after a successful delivery. A `try/finally` around the existing callback call will also clear it on failure and cancellation while preserving payload, result, and error identity. I’ll add regressions for those paths, retries, duplicate suppression, and independent instances.



Fixed `Sender.send` with `try/finally` so failures and cancellation clear `pending`, preserving argument, result, and error identity.

Extended `test_sender.py` without removing assertions. Coverage includes cleanup, duplicates, retries, independent instances, and opaque payload identity. Controlled tasks have bounded waits and cleanup.

Before the fix: 3 regression failures. Afterward, `python3 -B -m unittest discover -v`: **4 tests passed**, exit 0. `git diff --check` passed.

Validation was local, using cooperative callbacks. Only `sender.py` and `test_sender.py` changed; existing `.agents/` content was preserved.
