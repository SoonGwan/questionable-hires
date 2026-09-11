# Remaining conditional paths: preserved outcomes, no resource win

Execution snapshot `5167077`: Exorcist instructions `3ededb6`, Mother-in-law
`d1be060`. Two fresh Astra-medium skill sessions, serial, one each; no retry,
baseline or whole-team rerun. Raw evidence: ignored `local-runs/conditional-paths-01`.

| Case | Tokens, input including cache + output | Seconds |
| --- | ---: | ---: |
| search-diagnosis | 69,156 | 52.210 |
| search-protected | 68,022 | 52.612 |

Total 137,178 tokens / 104.822 seconds. Against screen 05's same two cases:
1.2% more tokens and 25.3% more time. No aggregate efficiency win. These separated
single samples do not isolate instruction effects; screen 05 had different
termination safeguards and artifacts.

Exorcist demonstrates both actual Search/transport completion orders with a
cache-free request and verifies no-cache headers. It does not read or invoke the
optional runner. Signal/task/cleanup waits use asyncio timeouts, but there is no
process deadline: cancellation-resistant behavior is not contained by this artifact.
The current implementations are cooperative, so the observed diagnosis succeeds;
do not claim this branch establishes general cancellation-resistant robustness.

Mother-in-law uses actual Search state, verifies both completion orders, and does
not invent a stale-result defect. Its retained `qa_search.py` includes a parent
five-second subprocess deadline and reports expiration as INCOMPLETE. The final
command `python3 -B qa_search.py` preserves the deadline. Browser behavior remains
explicitly untested; worker-only invocation would bypass the parent protection.

## Evidence integrity

New automatic inventories record all six installed resource instances before
and after; none changed. Author comparison of those hashes with `5167077` blobs
matches. All three original fixture files across the two cells remain unchanged.
No rejected patches or invalid JSON.

The diagnosis's complete original output is captured. Protected search records
exit 0 with empty output, flagged by diagnostics; this alone does not establish
the described observations. Separate author replay of both retained scripts
returns exit 0 and prints their two expected sequences. The protected-search detail
is therefore independently replayed artifact evidence, not retroactively credited
to missing original model output. No new adversarial model test was run.

Disposition: remaining task paths are checked, with distinct termination and
capture limits. Neither lower instruction length nor correct conclusions establish
the requested broad performance gain. Keep the adverse cost record; another
unchanged-set run is not justified by these results.
