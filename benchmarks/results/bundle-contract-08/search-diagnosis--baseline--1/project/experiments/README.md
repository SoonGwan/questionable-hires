# Search completion-order experiment

Run from the project root using the installed Python (standard library only):

```sh
python3 experiments/search_completion_order.py
```

The captured successful run is `search_completion_order.results.json`. To refresh it:

```sh
python3 experiments/search_completion_order.py > experiments/search_completion_order.results.json
```

The experiment imports the actual `Search` and `transport.fetch`. Only the injected
request callable is a controlled in-memory stub. It records URL, query parameters,
and headers, and returns unique query-specific responses without a cache. Both
requests are confirmed in flight before responses are released. Events and futures
control ordering; no timing sleeps are used. Behavior-dependent waits have a
two-second timeout. A `finally` block cancels unfinished owned tasks and futures
and drains the tasks with a bounded wait, including on failures.

## Local evidence

| Request issue order | Controlled completion order | Final Search.result |
| --- | --- | --- |
| older, newer | older, newer | newer (current) |
| older, newer | newer, older | older (stale) |

All four recorded requests target `/search` with the correct `q` and
`Cache-Control: no-cache`. Assertions verify headers, each intermediate result,
and the expected final outcome. In the normal case the older result also appears
temporarily while the newer request is pending.

`Search.run` unconditionally assigns each awaited response to `self.result`.
There is no latest-query check, so the last response to complete wins even when
it belongs to the earlier query. Reversing only completion order reproduces the
reported stale-result pattern with no cache present.

## Limits and preservation

This establishes a race in the supplied code when overlapping calls share a
Search instance. It does not establish how often production calls overlap or
prove that production incidents have no additional causes. Real request clients,
servers, caches, and UI lifecycle behavior were not exercised. A recorded request
header alone does not establish production cache behavior.

No production fix was made. SHA-256 hashes before and after the run matched for
`search.py` and `transport.py`; `git diff` also confirmed both files unchanged.
All added artifacts are under `experiments/`. No dependencies or external
services are required, and imports do not write bytecode files.
