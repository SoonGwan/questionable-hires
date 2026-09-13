# Scoped cookie clearing: new development transfer

Freeze Con Artist at `36e201c`; source is full HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177`, using the existing
`/tmp/qh-httpx-preflight.3Slnqw/venv/bin/python` environment. No upstream files,
tests or dependency versions are changed. This is an author-selected new task
within an already exposed project, not an independent maintainer holdout.

Run `run_httpx.py --profile cookies-audit --arms baseline skill --repeats 1`
with explicit source/interpreter and unused output directory. Two fresh serial
GPT-6 Astra medium sessions, seed 20260912, 360 seconds each. Preserve both
scheduled cells, failures and repairs; no retries for a favorable result. Do not
run author regression tests concurrently with model timing.

The request concerns path-scoped clearing and retention of other-path and
other-domain cookies. Require inspection of relevant real code/assertions, a
passing original cookie suite, one isolated behavioral fault, and the detecting
assertion or a stronger assertion passing correct/failing faulty code if missed.
Also require domain-only clearing control on correct and faulty code, retaining
the other domain's actual cookie identity/value. Do not equate one killed fault
with complete coverage of all scoping contracts. Existing files must remain
unchanged; inspect commands, imports/caller provenance, final snapshots and scope.
An audit does not request implementing a production fix or publishing artifacts.

Author preflight with [the oracle](httpx-cookies-oracle.json): 7 correct tests
pass. Ignoring the path argument in `Cookies.clear` gives 1 actual assertion
failure / 6 passes: `test_cookies_with_domain_and_path` at line 50 observes
`len(cookies) == 0`, expects 1. Both domain-only controls preserve exactly
`('example.org', '/one', 'other', 'C')`. Four completed helper phases, no timeout
or truncated output; copied implementation import checked in every phase.
This recipe and its result stay outside the evaluated project and model prompt.

Review total input (cached included once) plus output tokens and process wall
time, as well as actual work, failures, controls and evidence. Report lower cost
only with its observed comparability limits; n=1, shared host/cache, order and
one authored task cannot prove broad gains. Current routing's `--full` adoption
may be observed, but the short cookie test file cannot establish its large-file
benefit. No featured scores or bilingual charts change from this diagnostic pair.
