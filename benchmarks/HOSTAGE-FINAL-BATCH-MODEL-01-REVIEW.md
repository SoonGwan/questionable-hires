# Final batching adoption 01 — fewer calls, partial original test transcript

2026-09-14, launch `d035f34`, resources `fc557ad`.
[Frozen protocol](HOSTAGE-FINAL-BATCH-MODEL-01-PROTOCOL.md);
[retained evidence](results/hostage-final-batch-model-01/).
One fresh explicit-skill Astra medium session on the unchanged exposed keyed-import
task. No retry or baseline; no author tests or edits during model timing.

## Observations, not causal gains

| Recorded measure | Keyed import 01 (`6d0d108`) | This screen |
| --- | ---: | ---: |
| Total input + output tokens | 118,971 | 95,992 |
| Process wall time | 103.161s | 94.261s |
| Shell tool calls | 6 | 4 |
| Finalization calls | 3 | 1 |

Tokens are **19.31% lower**, time **8.63% lower** descriptively. Current usage is
93,288 input + 2,704 output; cached input is included once. These are two single
sessions, shared host/cache, different generated test grouping/extra assertions
and two instruction changes. They do not isolate causality or establish a general
20–30% gain. The task remains authored/exposed, not independent external work.

## Original execution and adoption

The model reads the full Python callback asset and copies it once. It groups
native tests, cmp, unchanged-original-test diff, whitespace check, scoped diff
and status with `&&` in item 6. Final shell exit is zero; no later check masks an
earlier failure. The command also writes the new test file before those checks.
Only four shell calls are observed. Item 5 is a legitimately empty copy command.

**Capture gap:** item 6 reports `Ran 10 tests ... OK` (0.059s), but its retained
output starts with a bare `ok` and includes only five full verbose test headers.
The runner flags this discrepancy. There is no earlier complete transcript to
reuse and no original rerun. Do not claim ten individually captured original
test results or use author replay to fill those missing lines. No initial failing
test command is observed in the available record.

Actual production code matches the prior simple per-key implementation: mark
before fetch, suppress duplicate key, preserve active result/error semantics,
remove only its own key in finally. Requirements and both original tests are
unchanged. Only importer.py changes plus controlled_call.py and test_importer.py
are added. Raw terminal usage, normalized events, resource hashes, copied asset
and full inventory reconcile. No observed scope exception.

Generated tests use `started_before` with the appropriate application tasks.
Dependent fetch/persist steps are sequential, without continuing subtest wrappers.
Six interruption scenarios are separate native tests calling a shared helper.
Tests cover duplicate entry in both phases with unspecified result, equal string
keys, independent keys/instances, active payload/result/error semantics, synchronous
and asynchronous failures in both phases, recovery and actual cancellation. They
snapshot busy sets and other-call fields and exercise the other key to completion.
Cleanup is registered before waits and now has its own cooperative one-second
cancel/gather bound; arbitrary cancellation suppression is still not contained.

## Separate unchanged-test replays

[Six author replays](results/hostage-final-batch-model-01/author-replay.json)
retain every original generated assertion and apply only production variants in
disposable project-local copies, 20-second process bounds. Each discovers ten
native tests; none times out. Original retained files are unchanged.

| Variant | Separate native observation |
| --- | --- |
| Final | 10 pass, 0.062s |
| Valid duplicate return False | 10 pass, 0.060s |
| Original missing busy state | 2 pass, 8 missing-attribute errors |
| Missing guard | 9 pass, 1 actual unexpected-callback-list failure |
| Missing cleanup | 2 pass, 8 busy-set failures |
| Blocks other keys | 3 pass, 7 entry/result/expected-error failures |

All expected variant outcomes match. No `UnboundLocalError` appears, unlike the
three faulty variants in the original keyed-import tests. Duplicate fault output
retains actual calls `[('catalog',), ('catalog', None)]` versus expected `[]`.
Independent-key blocking produces early `EntryNotObserved` among its failures.
These are useful adoption observations and clean fault diagnostics in this output,
not proof against every fault, a repaired original transcript or a global score.

The replay tool adds an explicit `final-batch-01` profile with the frozen resource
and ten-test expectation; its prior six-test default is preserved and rerun in
separate scratch. No historical export or chart is regenerated.

## Remaining objective

Final-call batching and dependent-phase failure boundaries are actually adopted
in this model output. Whole-task efficiency remains provisional because work and
capture differ; all-eight external developer gains are still unproven. Preserve
the partial transcript and prior adverse results. No further identical favorable
retry, new skill rule or featured promotion is justified by this screen alone.
