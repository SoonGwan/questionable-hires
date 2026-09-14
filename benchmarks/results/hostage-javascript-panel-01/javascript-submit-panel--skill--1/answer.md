I’ll use the hostage-negotiator skill to keep this focused on `SubmitPanel` state and regression coverage. I’ll read the project requirements and existing tests first.



`SubmitPanel` currently just awaits `save`. I’ll add an instance-level pending guard and clear it in `finally`. The new tests will use controlled callbacks with deadlines and cleanup, while leaving both existing tests unchanged.



All seven tests passed, including the two existing tests. The new coverage checks pending state, duplicate suppression, independent instances, identity preservation, and retry after asynchronous failure, synchronous failure, and abort-triggered rejection. I’ll check the final diff for scope and confirm the original test file is unchanged.



Implemented `SubmitPanel.pending` with per-instance duplicate suppression and `finally` cleanup after success or failure, preserving the existing API and identities.

Added five rerunnable native regression tests covering all requested scenarios, with bounded waits, prompt rejection handling, and callback cleanup. Both existing tests remain unchanged.

Verification: `node --test` passed all 7 tests; diff checks passed.
