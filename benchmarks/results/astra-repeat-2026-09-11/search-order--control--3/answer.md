I’ll inspect the search flow and existing tests, then add a deterministic local reproduction for any realistic failure I find without changing production code.

The requirements say the latest query’s result must remain visible. `Search.run` assigns every response directly, so an older request could overwrite a newer result if it finishes last. I’ll test that ordering with controlled local responses and no timing delays.

Reproduced a stale-response bug: typing `cat`, then `cats`, displays the older `cat` result when its request finishes last.

Added `test_search.py` using controlled async responses, with no sleeps or external services.

Verified with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search`: fails at the assertion that the latest result remains visible, confirming the bug.

Production code is unchanged.
