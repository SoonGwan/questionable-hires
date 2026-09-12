# Real checkout inspection: focused hunks did not transfer; shallow fix

Six author-selected HTTPX ranges were compared with the prior collector and
`c84379c`. Attribution, current code, status and commit IDs matched, but no hunks
were omitted and four outputs still truncated. This is an unfavorable transfer
result for the focused-hunk optimization, not six model successes.

The prepared checkout at `26d48e0634e6ee9cdc0533996db289ce4b430177` is shallow
(`rev-parse --is-shallow-repository`: true; `rev-list --count HEAD`: 1). All six
ranges attribute to a boundary. Git renders missing-parent history as apparent
whole-file additions. Those patches cannot establish the real introducing change.

The new candidate requests metadata without a patch for shallow-boundary commits,
adds `patch_unavailable`, and retains current text and line attribution unchanged.
Genuine roots in complete histories still return patches. No history was fetched.

| File / current lines | Prior commit-evidence characters | Candidate metadata characters |
| --- | ---: | ---: |
| `httpx/_transports/asgi.py` 90 | 5,965 | 101 |
| `httpx/_transports/wsgi.py` 32 | 5,251 | 101 |
| `httpx/_client.py` 502–503 | 12,000 | 101 |
| `httpx/_client.py` 542–543 | 12,000 | 101 |
| `httpx/_client.py` 552–556 | 12,000 | 101 |
| `httpx/_models.py` 969–972 | 12,000 | 101 |

These count only `commits[].evidence`, not complete JSON, tokens or time. Six
ranges share the same truncated history; they are not independent repositories.
All show the missing-parent limitation explicitly. This removes misleading bulk,
not missing historical information; current necessity still requires callers/tests.

Fifteen collector tests pass, including shallow metadata preservation and genuine
root patch retention. Full suite: 132 tests pass in 12.647 seconds; repository and
skill validators pass. No model performance result or broad completion claim.
