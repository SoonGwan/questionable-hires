# Search completion-order experiment

The supplied `Search.run` unconditionally assigns each completed fetch to
`self.result` (`search.py:5`). An older in-flight search can therefore overwrite
a newer result. The local experiment reproduces this with no cache involved.

Run from the project root, using only Python's standard library:

```sh
python3 -B experiments/search_order.py
```

The successful run's recorded output is in `evidence.json`. To refresh it:

```sh
python3 -B experiments/search_order.py > experiments/evidence.json
```

The harness imports the actual `Search` and `transport.fetch`. Only the injected
request function is a stub: it records URL, query parameters, and headers, then
waits on a separate controlled response gate for each request. It performs no
network calls and implements no caching. Both scenarios submit `older` then
`newer` and wait until both requests are in flight before releasing responses.

| Completion order | Final visible query | Outcome |
| --- | --- | --- |
| older, newer | newer | Current result |
| newer, older | older | Stale overwrite reproduced |

Every recorded request targets `/search`, carries the correct query parameter,
and has `Cache-Control: no-cache`. Assertions verify these arguments, intermediate
visible results, and final outcomes. Each behavior-dependent wait has a two-second
deadline. A `finally` block cancels pending owned tasks and response gates, retrieves
task exceptions, and bounds task cleanup. No timing sleeps determine ordering.

This demonstrates that completion ordering alone is sufficient to cause the bug
in this project. It does not prove that the observed production incidents followed
this sequence, nor does it rule out additional cache issues. The recorded header
shows what this transport passes to its request dependency; there is no real HTTP
client, server, intermediary, or production trace here to establish actual cache
behavior. Production diagnosis would require correlating query submission,
response completion, and result assignment for affected searches.

No production fix was made. The initial working tree was clean; after the run,
only `experiments/` was untracked and the production-file diff was empty. The
harness also records SHA-256 hashes and asserts that `search.py` and `transport.py`
remain unchanged during execution.
