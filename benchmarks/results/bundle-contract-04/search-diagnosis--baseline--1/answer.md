I’ll inspect Search and its transport, then build a rerunnable local experiment with controlled response ordering. I’ll preserve production files and existing changes.

`Search.run` assigns every completed response to the shared result, with no check for a newer query. The transport sends `Cache-Control: no-cache`. I’ll test whether reversing response order reproduces the stale result using a controlled request stub with no cache.

Reproduced an **out-of-order response race** using actual Search and transport with a cache-free request stub:

- Normal completions leave the newer result.
- Reversed completions let the older response overwrite it.
- All recorded requests include `Cache-Control: no-cache`.

Caching isn’t required to reproduce the symptom; production cache behavior remains unverified.

Rerun: `python3 -B experiments/search_race.py`

Evidence and explanation are in `experiments/search_race_results.json` and `experiments/README.md`. Checks passed, waits are bounded, owned tasks are cleaned up, and production files are unchanged.
