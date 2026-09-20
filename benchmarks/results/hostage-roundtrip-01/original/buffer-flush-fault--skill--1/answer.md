I’ll use the hostage-negotiator skill to review the contract, add focused native tests, and change `buffer.py` only if I find a contract defect.

I found a contract defect: failure recovery overwrites items added during the send. It must prepend the detached batch to those additions. I’ll cover async failure, cancellation, and synchronous failure, plus suppression, success, identity, and buffer independence.

The baseline run confirmed lost additions in four tests; all seven tests terminated, including failure cleanup. I’ve changed recovery to prepend the detached batch and will run the suite again.

Fixed one contract defect in `buffer.py`: failure recovery now restores the batch before concurrent additions instead of discarding them.

Added seven native tests covering all requested scenarios, with observed callback entry, bounded waits, and owned-task cleanup. No timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests passed, process exit 0**.

Preserved `requirements.md`, `AGENTS.md`, and unrelated notes.
