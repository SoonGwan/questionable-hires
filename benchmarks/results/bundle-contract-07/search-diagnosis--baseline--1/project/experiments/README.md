# Search response ordering experiment

Run from the project root with the existing Python standard library:

```sh
python3 -B experiments/search_order.py
```

The command asserts the observed behavior and regenerates
`experiments/search_order_results.json`, including request arguments, state after
each completion, and before/after SHA-256 hashes of both production files.

The experiment imports the actual `Search` and `transport.fetch`. Only the
injected `request` boundary is replaced with an in-process double. It has no
cache and returns a distinct, query-specific value for each request. Both
queries reach that boundary before either is released. Arrival and task waits
have two-second deadlines; all owned search tasks are cancelled if necessary
and drained in `finally`. No sleeps, dependencies, or external services are used.

Observed results (both requests start in the order `old`, then `new`):

| Completion order | Result after each completion | Final result |
| --- | --- | --- |
| `old`, `new` | `old`, `new` | `new`, current |
| `new`, `old` | `new`, `old` | `old`, stale |

In both scenarios the recorded calls target `/search`, carry the correct `q`
parameter, and include `Cache-Control: no-cache`.

The local cause is `search.py:5`: each invocation unconditionally assigns its
response to the shared `result` after awaiting the fetch. An older invocation
can resume after a newer one and overwrite its result. There is no check of
which query is latest. Response order alone is sufficient to reproduce the
reported symptom; a cache is unnecessary for this reproduction.

This is evidence about the supplied synthetic implementation, not a production
incident trace. The double records transport arguments, not wire traffic. The
experiment does not establish whether production callers overlap searches on
the same instance, how requests complete in production, or how any HTTP client,
server, intermediary, or cache behaves. The recorded header alone does not
establish that production cache behavior is correct. Production diagnosis would
need correlated query starts, response arrivals, and result writes, plus cache
evidence if that remains a hypothesis.

No production fix was made. Production hashes were unchanged during the run,
and the tracked production files have no Git diff. The experiment and its report
are the only added files.
