I’ll inspect the search flow and local test setup, then test overlapping requests with controlled futures without changing production code.

`Search` uses a generation counter to reject results from older requests. I’ll test both completion orders, starting both with no result and with an existing result, and check the displayed value while the newer request is still pending.

No stale-result defect reproduced. All four tests passed using actual `Search` with controlled futures.

- Both completion orders leave the newer result displayed.
- Older completion while newer remains pending does not change the display.
- An existing result stays displayed until the newer request completes.

Tests use bounded event/task waits and clean up owned tasks. Production `search.py` is unchanged, verified by SHA-256.

Rerunnable test: [test_search_overlap.py](project/test_search_overlap.py)

```sh
python3 -B -m unittest -v test_search_overlap
```
