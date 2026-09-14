# Friday commit-before-ack transfer screen 01 — 2026-09-14

Skill resources `f15f3ae` (unchanged at author source `3fa1fd1`). New fixtures
`friday-ack-cases.json` SHA-256
`4e746de6d34b5b5d06955546e8cdc77d14042a2f98e2b45465ac4aba99d133b4`.
The earlier writer fixture stays frozen, including its acknowledgment ambiguity.

## Actual caller and local controls

Two related scenarios reuse the old schema/version functions, adding an actual
application entrypoint that commits, closes its connection, then acknowledges.
Readers use independent fresh connections. Failed transactions raise, not return
acknowledgment. Supplied release/task states sequential calls, update existing
keys, insert fresh keys, cross-version visibility after each acknowledged write,
and preservation after documented down. No concurrent ordering, crash durability,
production readiness or unprovided application layer is claimed.

Preflight uses real generated application/version modules and a project-local
disk database. Old update 20, new update 30, old insert 40, new insert 50 produce
cross-version observations `[10,20,null,50]` in gap and `[20,30,40,50]` in control.
After down, old reads return `[20,40,50]` versus `[30,40,50]`. An attempted duplicate
insert raises IntegrityError and leaves its previous value intact in both cases.
Removing the actual transaction context makes close roll back before the success
dictionary returns; a native unittest fails with `AssertionError: 10 != 20`.
Two author tests pass (0.159s), covering both expected scenarios and that intended
failure. Source files are unchanged; scratch DB is under the disposable project.
These are fixture controls, not model results or unseen-independent holdout tests.

## Frozen execution and review

Four fresh Astra medium sessions, baseline/skill on both cases, n=1/arm/case,
jobs=1, seed20260911, 240 seconds/cell. No favorable retry. No resource/fixture
changes or author tests during timing. No previous solutions in prompts. Preserve
all cells, errors, timeouts, unknown usage and account-limit unattempted cells.

Review actual source reads, application entrypoint use and function bindings,
independent-connection values for every write kind, documented rollback and
post-down values, original-file preservation and project-local scope. Report
observed defects for gap; don't manufacture a local compatibility failure for
control or infer production readiness. Helper use is not required; a SQL-only
matrix is not a substitute for the supplied writers. Inspect original outputs,
not prose success; separate unchanged-program replay must not fill original gaps.
Reconcile raw usage, frozen installation bytes/modes and final inventories.

Report each arm and both cases, including adverse efficiency/false positives.
This is a related authored transfer screen, not a broad 20–30% or causal claim.
Do not change historical/featured charts. Update dated EN/KO results only after
review. The prior favorable schema pair is not the success threshold for this run.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/friday-ack-cases.json --output benchmarks/local-runs/friday-ack-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
