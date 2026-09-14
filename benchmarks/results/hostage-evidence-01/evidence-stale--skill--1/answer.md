I’ll use the hostage-negotiator skill to inspect the pending-state change and handoff evidence, then run the project’s native checks if no matching report is usable. I’ll preserve the existing tests, support files, and original handoff evidence.

`submit()` sets `pending` but never clears it because its `finally` block contains `pass`. I’ll restore cleanup there. The saved report records six passing tests, but its source fingerprint differs from the current file; I’ll check all recorded inputs again after the fix before relying on it.

Ready. Restored `pending = False` in `form.py`’s `finally` block, ensuring cleanup on success, failure, and cancellation while preserving duplicate suppression.

Verification reuses `verification/prior.json`: its command, interpreter, and every source/test fingerprint match the corrected files. It records **6 tests passed, exit 0**. No new suite run occurred; the original missing transcript remains unavailable.

Tests, support files, and handoff evidence are unchanged. `git diff --check` passed.
