I’ll use the hostage-negotiator skill to review the contract, add controlled native tests, and change `buffer.py` only if I find a real defect.

I found a recovery defect: failure or cancellation replaces the waiting queue with the detached batch, losing items added during the send. I’ll add tests for that behavior and the other requested contracts, then fix restoration to prepend the failed batch.

Fixed one contract defect: failure and cancellation now restore the detached batch before concurrent additions instead of discarding them.

Added 7 native unittest tests covering all requested scenarios, with observed callback entry, bounded waits, owned-task cleanup, and no timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests passed, process exit 0**. Before the fix, 4 tests failed on lost additions.

Preserved `requirements.md`, `AGENTS.md`, and owner notes. No scratch files remain.
