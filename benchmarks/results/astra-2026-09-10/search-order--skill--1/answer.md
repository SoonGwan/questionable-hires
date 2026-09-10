I’ll use the mother-in-law skill to inspect the search flow and reproduce a realistic interaction failure with a deterministic local test. I’ll leave production code unchanged.

The requirements say the latest query’s result must remain visible. `Search.run` currently lets every completed request replace that result, so I’ll test an older request finishing last. This project has no browser harness; I’ll test the asynchronous state that the screen displays.

Found one defect: **older responses overwrite the latest search result**.

- Sequence: type `ca`, then `cat`; complete `cat` first, then `ca`.
- Expected: `["cat"]` remains visible.
- Observed: `["car", "cat"]` replaces it. An older response also repopulates a newer empty result.

Added deterministic tests in [test_search.py](project/test_search.py), using controlled futures without sleeps or network calls.

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search`

Result: **2 failing reproductions, 1 passing control**. Production code unchanged. Tested the displayed state boundary; no browser journey was exercised.
