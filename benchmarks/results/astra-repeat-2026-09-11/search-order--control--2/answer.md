I’ll inspect the search flow, identify a realistic interaction failure, and add a deterministic local reproduction without changing production code.

The requirements say the latest query’s result must stay visible. `Search.run` assigns every response directly, so an older request appears able to overwrite a newer result. I’ll test that completion order using controlled futures, with no network calls or timing delays.

Reproduced a stale-response bug: type `ca`, then `cat`; if `cat` finishes first, the later `ca` response overwrites its results.

Added deterministic regression test in [test_search.py](project/test_search.py), using controlled futures without sleeps or network access.

Verified with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search`. It fails at the final assertion as expected, displaying `ca result` instead of `cat result`.

Production code is unchanged.
