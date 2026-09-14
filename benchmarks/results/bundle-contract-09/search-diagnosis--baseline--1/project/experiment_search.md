# Local search diagnosis

The synthetic project's `Search.run` unconditionally assigns the response when
`fetch` completes (`search.py:5`). Concurrent calls on one Search instance thus
make the last response to complete win, even when it belongs to an earlier query.

## Reproduce

From this project, run:

```sh
python3 -B experiment_search.py
```

To refresh the saved evidence:

```sh
python3 -B experiment_search.py > experiment_search.results.json
```

No dependencies or network are required. The experiment imports the actual
`Search` and `transport.fetch`, substituting only the injected request callable.
It starts `earlier`, waits until its request is recorded, then starts `newer` on
the same Search instance. Both requests are pending before either is released.
Events control completions without timing sleeps. Every behavior-dependent wait
has a two-second timeout; a finally block cancels and gathers owned tasks even
on assertion failure or timeout.

## Recorded local evidence

| Request start order | Controlled completion order | Result after each completion | Final result |
| --- | --- | --- | --- |
| earlier, newer | earlier, newer | earlier, newer | newer (current) |
| earlier, newer | newer, earlier | newer, earlier | earlier (stale) |

In both cases the actual transport called `/search` twice with the respective
`q` parameters and `{"Cache-Control": "no-cache"}` headers. The request stub
returned fresh, query-specific data and implemented no cache. Assertions passed
for request contents, completion order, intermediate results, and final results.
All owned tasks finished. Full headers, snapshots, and source hashes are in
`experiment_search.results.json`.

This demonstrates a response-order race sufficient to explain the symptom in
this project. A cache is not necessary for the reproduced failure.

## Production uncertainties and preservation

This experiment observes headers at the injected request boundary, not on a real
network. It does not establish how any deployed HTTP client, proxy, server, or
cache behaves, nor does the header alone prove that production caching is absent.
It also does not establish whether deployed callers reuse one Search instance,
allow overlapping searches, cancel earlier work, or gate result rendering.
Production traces linking input order, response order, and result updates would
be needed to attribute an actual user incident to this race or assess additional
cache problems.

Neither production file was edited. SHA-256 hashes matched before and after the
run, and `git diff --exit-code -- search.py transport.py` passed. The initial
working tree was clean. Only this report, the experiment, and its recorded output
were added; no fix, installation, external service, publishing, or deployment
was performed.
