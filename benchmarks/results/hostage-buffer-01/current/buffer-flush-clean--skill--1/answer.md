I’ll use the hostage-negotiator skill to review the contract, add controlled async unittest coverage, and change `buffer.py` only if the review or tests expose a real defect.

`buffer.py` appears to satisfy the contract, including restoring failed batches ahead of new additions and clearing `busy` on cancellation. I’ll leave it unchanged and test those transitions using the skill’s local callback helper, with bounded waits and task cleanup registered before each task starts.

The tests now cover suppression, receipt and item identity, ordered restoration and retry after all three failure modes, and independent buffers. They wait for actual callback entry without sleeps, and owned tasks are cancelled and drained in cleanup even if an assertion fails. I’m running the requested unittest command now.

No contract defects found; `buffer.py` remains unchanged.

Added 7 native unittest tests and local callback support covering all requested scenarios, bounded waits, and task cleanup without timing sleeps.

`python3 -B -m unittest discover -v`: **7 tests passed**, **process exit 0**.

Preserved `requirements.md`, `AGENTS.md`, and owner notes.
