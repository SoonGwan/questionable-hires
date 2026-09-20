I’ll use the hostage-negotiator skill to review the contract, add controlled native tests, and change `buffer.py` only if the review reveals a real defect.


I found a contract defect: failure recovery replaces the waiting queue with the failed batch, discarding items added during send. I’ll add tests that expose this for async failure, cancellation, and synchronous callback failure, then fix restoration order.


The tests reproduced the queue-loss defect in four cases. The one-line fix prepends the failed batch to the waiting queue, and all seven native tests now pass. I’m checking the final diff and file scope.


Fixed one contract defect in `buffer.py`: failure recovery now restores the batch before concurrent additions without discarding them.

Added seven native tests covering all requested scenarios, with controlled callback entry, bounded waits, and task cleanup. No timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests passed, process exit 0**. Before the fix, four tests failed.

Requirements, instructions, and owner notes remain unchanged.
