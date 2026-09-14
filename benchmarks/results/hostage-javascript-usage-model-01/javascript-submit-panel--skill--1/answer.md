I’ll use the hostage-negotiator skill to keep the change focused, read the project requirements, and add rerunnable regression tests while preserving the existing tests.



The requirements place pending state on each panel instance and leave cancellation to the save callback. I’ll guard callback entry and clear pending in `finally`, then test the required transitions with controlled promises and bounded cleanup.



Implemented `SubmitPanel.pending` with per-instance duplicate suppression and cleanup after success, synchronous errors, and rejected saves, including abort-triggered rejection. The existing API and object identities are preserved.

Added five bounded regression tests with callback settlement and task cleanup. Both existing tests remain unchanged.

`node --test`: all 7 tests passed.
