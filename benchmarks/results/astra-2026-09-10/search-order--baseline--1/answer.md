I’ll inspect the search flow, look for a realistic interaction failure, and add a deterministic local reproduction without changing production code.

The search stores every response as it arrives, so an older request can overwrite the latest query’s result. I’ll reproduce that by starting searches for `ca` and `cat`, then completing `cat` first and `ca` second using controlled local futures.

Reproduced a stale-result race: type `ca`, then `cat`; if `cat` finishes first, the slower `ca` response overwrites it.

Added [test_search.py](project/test_search.py), using controlled futures without sleeps or network access.

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search.py`

Result: **1 test failed**, confirming the bug. Production code is unchanged.
