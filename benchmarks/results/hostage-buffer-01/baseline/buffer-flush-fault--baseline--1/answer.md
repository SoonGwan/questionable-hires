I’ll read the contract and implementation, add deterministic unittest coverage, and change `buffer.py` only if I find a contract defect.

The failure path has a contract defect: it replaces the waiting queue with the failed batch, losing items added during the send. I’ll add tests for that restoration behavior, plus suppression, identity, cancellation, retry, and buffer independence. Callback-entry events and bounded waits will control the tests without sleeps.

The tests reproduced the queue loss on synchronous failure, async failure, and cancellation: four tests failed, with process exit 1. I’ll fix the restoration to prepend the failed batch, preserving all newer items in order.

Fixed one contract defect: failure restoration now prepends the detached batch, preserving concurrent additions.

Added 7 native unittest tests covering all requested scenarios, with callback-entry synchronization, bounded waits, and task cancellation/draining on assertion failure. No timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests passed; process exit 0**. Before the fix, 4 tests failed.

Only `buffer.py` and new `test_buffer.py` changed; requirements, instructions, and owner notes were preserved.
