I’ll inspect the search flow, identify a realistic interaction failure, and add a deterministic local test without changing production code.

The code allows an older request to overwrite a newer result if it finishes last. That violates the requirement that the latest query’s result remain visible. I’ll reproduce this with an async test that controls completion order using events, without sleeps or network access.

Reproduced a stale-result bug: type `ca`, then `cat`; if the `ca` request finishes last, it overwrites the visible `cat` result.

Added [test_search.py](project/test_search.py), using async events for deterministic ordering—no sleeps or external services.

Verified with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search`: fails at the final assertion, showing `Results for ca` instead of `Results for cat`.

Production code is unchanged.
