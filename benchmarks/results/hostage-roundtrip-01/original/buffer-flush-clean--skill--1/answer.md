I’m using the hostage-negotiator skill to check the contract, fix any demonstrated defects, and add controlled native tests within the permitted scope.

`buffer.py` appears to satisfy the contract, including restoring batches after failure or cancellation. I’ll leave it unchanged and test those transitions with controlled callbacks, bounded waits, and cleanup registered before tasks start.

No contract defects found; `buffer.py` remains unchanged.

Added seven native unittest tests covering the requested behavior, using actual callback entry, bounded waits, and owned-task cleanup without timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests passed, process exit 0**.

Requirements, project instructions, and unrelated owner notes were preserved.
