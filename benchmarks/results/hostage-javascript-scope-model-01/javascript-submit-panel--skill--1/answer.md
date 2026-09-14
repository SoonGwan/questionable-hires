I’m using the hostage-negotiator skill to keep the change focused. I’ll read the project requirements and existing tests, implement the pending lifecycle, and add bounded regression tests.



The requirements fit a per-instance boolean and a `try/finally` around the existing save call. I’ll leave both existing tests unchanged and use the skill’s controlled-call helper for the new tests, so failed checks still release callbacks and drain submissions.



Implemented `SubmitPanel.pending` with per-instance duplicate suppression and cleanup after success, failure, or callback rejection on abort. Existing API and signal/result/error identities are preserved.

Added five bounded regression tests with callback settlement and task draining. Both existing tests remain unchanged.

`node --test`: all 7 tests passed.
