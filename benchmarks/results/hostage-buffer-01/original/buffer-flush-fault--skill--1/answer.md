I’ll use the hostage-negotiator skill to review the contract, change `buffer.py` only if needed, and add controlled native tests with bounded waits and task cleanup.

I found a contract defect: failure recovery replaces the waiting queue, discarding items added during the send. I’ll add tests for restoration order and the other requested transitions, then fix that recovery line.

The tests reproduced lost additions on async failure, cancellation, and synchronous failure. The one-line fix prepends the restored batch to the waiting queue. All seven native tests now pass; I’ll check the final diff and file scope.

Fixed one contract defect in `buffer.py`: recovery now restores the batch before concurrent additions without discarding them.

Added seven native tests covering all requested behaviors, with observed callback entry, bounded waits, and task cleanup. No timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests passed, process exit 0**.

Preserved `requirements.md`, `AGENTS.md`, and unrelated notes.
