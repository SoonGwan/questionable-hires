I’ll inspect the search flow, look for a realistic interaction failure, and add a deterministic local reproduction without changing production code.

The flow appears vulnerable to out-of-order responses: an older query can finish last and overwrite the latest result. I’ll test this by holding the first response until the second query has completed, using explicit synchronization rather than timing delays.

Reproduced a stale-response bug: typing `ca`, then `cat`, shows the correct `cat` results initially, but the slower `ca` response overwrites them.

Added `test_search.py` with deterministic event synchronization—no sleeps or external services.

Run:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search.py
```

Result: **1 test fails**, confirming the latest-query requirement is violated. Production code is unchanged.
