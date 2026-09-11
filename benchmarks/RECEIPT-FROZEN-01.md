# Frozen assertion behavior check

One fresh `receipt-changed-tests` skill session at `4d9b380`, Astra medium,
serial, with no baseline comparison or retry. Local evidence remains under
ignored `local-runs/receipt-frozen-01`. This is an authored development case,
not a held-out or performance benchmark.

The agent fetched `HEAD:test_totals.py` once, wrote identical bytes into both
isolated copies, and varied only `totals.py` from `HEAD^` versus `HEAD`.
Its command printed each revision and subprocess exit code independently.
The exact-minimum assertion failed on `39d21b3` with `False is not true`, exit
1, and passed on `168c05d`, exit 0. Neighbor assertions passed in both copies.
The agent did not substitute the older incomplete test suite as before evidence.

Original fixture bytes and the instruction digest were independently compared
after the run; they match. The recorded diff is empty, no receipt temporary
copies remain, and the command trace stays within the project. The actual
comparison and failure reason were reviewed in the trace, not inferred merely
from a successful wrapper exit. No additional independent execution of the
historical comparison was performed here.

Usage: 85,406 total tokens (84,608 input including cache + 798 output),
38.228 seconds. The earlier identical-historical-tests case is not an equivalent
cost comparison. This result supports adherence to the new frozen-assertion
guidance in one sample, not an efficiency win or proof that the old skill would
necessarily fail this case. Dirty-worktree and old-interface incompatibility
branches remain unverified.
