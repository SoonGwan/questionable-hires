I’ll read the hostage-negotiator skill and requirements, review `Preview.refresh`, and add deterministic unittest coverage. I’ll keep changes inside this project and run the requested command.


`refresh` publishes values only for the latest call, but its unconditional `finally` lets an earlier call clear `pending` while the latest is unresolved. I’ll guard that cleanup with the existing generation check and test the requested transitions using callback gates, bounded waits, and task cleanup.


All eight tests passed with process exit `0`. They cover both completion orders, failure and cancellation ownership, retry, synchronous callback failure, object identity, display retention, and instance isolation. I’ll now check the final diff and confirm the requirements and owner note are unchanged.


Fixed `Preview.refresh` so only the latest-started call clears `pending`. Overlapping calls remain independent.

Added eight deterministic unittest tests covering all requested cases, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes are unchanged.

Native verification: `python3 -B -m unittest discover -v` — **8 tests ran, all OK; process exit 0**.
