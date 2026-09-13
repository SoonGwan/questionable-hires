# Search response-order experiment

Run from the project root, using only the Python standard library:

```sh
python3 -B experiments/search_race.py
```

To refresh the saved evidence:

```sh
python3 -B experiments/search_race.py > experiments/search_race_results.json
```

The experiment imports the actual `Search` from `search.py` and `fetch` from
`transport.py`. Only the `request` callback is replaced with a controlled,
cache-free in-memory stub. It records path, query parameters, and headers
received from the real transport and returns a distinct result for each query.
Both searches use the same `Search` instance.

Event handshakes ensure the older request starts first and both requests are
pending before either is released. Every behavior-dependent wait has a two-second
timeout. Owned search tasks are cancelled if unfinished and gathered in `finally`,
also with a timeout. No sleeps, network access, or dependencies are needed.

## Observed local evidence

The saved `search_race_results.json` records a successful run:

| Controlled completion order | Result after first completion | Final result |
| --- | --- | --- |
| Older, then newer | Older query | Newer query (current) |
| Newer, then older | Newer query | Older query (stale) |

All four recorded requests use `/search`, the correct `q` parameter, and
`Cache-Control: no-cache`. Assertions check the exact requests, completion order,
intermediate results, and final stale/current outcomes. SHA-256 hashes confirm
`search.py` and `transport.py` are unchanged during the run.

The local cause is an out-of-order response overwrite: `Search.run` unconditionally
assigns each awaited response to `self.result`. An older pending search can finish
after a newer search and overwrite its result. The experiment reproduces this
without any cache, so caching is not necessary to produce this symptom.

## Production uncertainties

This establishes the race in the supplied implementation, not the cause of a
particular production incident. The project contains no caller/UI, real request
implementation, server, or cache to inspect. It remains unknown whether production
overlaps calls on a shared Search instance, cancels or filters stale responses
elsewhere, or also experiences cache issues. The recorded `no-cache` header alone
does not establish how a real cache behaves. Real timing, response headers, and
cache behavior were not exercised here.

No production code was changed. Only the experiment, this explanation, and its
recorded output were added under `experiments/`.
