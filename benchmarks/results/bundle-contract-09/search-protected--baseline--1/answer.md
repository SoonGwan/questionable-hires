I’ll inspect the local search flow and test setup, then add a rerunnable test with controlled completions without changing production code.

No stale-result defect reproduced. All four deterministic tests passed using actual `Search` with controlled futures.

- Both completion orders leave the newer result displayed.
- Older completion while newer remains pending does not update the display.
- An existing result stays displayed while loading.

Added [test_search_local.py](project/test_search_local.py) with bounded, behavior-dependent waits and owned-task cleanup. Production `search.py` is unchanged, verified by diff and SHA-256.

Rerun locally:

```sh
python3 -B -m unittest -v test_search_local
```
