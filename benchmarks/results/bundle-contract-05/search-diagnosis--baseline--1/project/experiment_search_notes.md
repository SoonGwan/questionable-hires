# Local search diagnosis

The synthetic project's `Search.run` unconditionally assigns each completed
response to `self.result` (`search.py:5`). With overlapping calls on one Search
instance, the last response to complete wins, even when its query is older.

The experiment imports and exercises the actual Search and transport. Only the
transport's injected `request` boundary is replaced with an in-memory stub. The
stub records the URL, parameters, and headers, and returns distinct query-tagged
responses through explicitly released futures. No cache or network is involved.

Both scenarios start `older`, wait for its request to arrive, then start `newer`
and wait for its request to arrive before releasing any response.

| Controlled completion order | Observed result sequence | Final result |
| --- | --- | --- |
| older, newer | older, newer | newer (current) |
| newer, older | newer, older | older (stale) |

All four requests used `/search`, the correct `q` parameter, and
`Cache-Control: no-cache`. Thus a cache is not necessary to reproduce this
failure. The captured header alone does not establish production cache behavior.

Production uncertainties: this project does not include a real request client,
server, cache, or UI caller. The experiment cannot establish whether production
calls overlap on a shared Search instance, whether responses arrive out of order
there, or whether caching also contributes. Production traces tying query,
invocation, response, and displayed-result order together would help confirm the
incident mechanism. No production fix was made.

Rerun from the project directory (Python standard library only):

```sh
python3 -B experiment_search.py > experiment_search_results.json
```

Assertions check request details, each visible result, and both final outcomes.
Request-start and task-completion waits have a two-second timeout. A `finally`
block cancels unfinished owned tasks/futures and waits up to two seconds for
task cleanup, including on failure. There are no timing sleeps or external
services. The recorded successful run is in `experiment_search_results.json`.
Before/after SHA-256 hashes match for both production files; their git diff was
also empty after the run. Only the experiment, its output, and these notes were
added.
