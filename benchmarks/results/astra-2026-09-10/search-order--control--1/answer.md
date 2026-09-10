I’ll inspect the search flow, look for a realistic interaction failure, and add a deterministic local test without changing production code.

The requirements say the latest query’s result must remain visible. The implementation assigns every response to the displayed result, so a slower earlier request appears able to overwrite a newer result. I’ll test that completion order using locally controlled futures, with no network calls or sleeps.

Reproduced a stale-result bug: typing `ca` then `cat` displays the `cat` results, but a slower `ca` response overwrites them.

Added [test_search.py](project/test_search.py) using controlled futures—no network or sleeps.

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search`

The test fails at the expected assertion in 10/10 runs. Production code is unchanged.
