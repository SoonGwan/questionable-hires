# Necessary history retained; repeated state checks remain costly

Four fresh Astra medium sessions follow the [frozen protocol](FRIDAY-HISTORY-PROTOCOL.md)
at snapshot `cb46fbe`, one repeat per case/arm, serial balanced order, no retries
or exclusions. Raw ignored evidence: `local-runs/friday-history-01`. Generated
cases are `local-runs/friday-history-cases-01.json`, reproducible from the committed
builder. Current project files are identical across the two cases; only deployed
worker history differs. This is development transfer, not confirmation data.

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| Historical incompatibility | 81,331 | 88,276 | 43.827 | 54.833 |
| Historically compatible worker | 81,430 | 86,160 | 49.984 | 47.313 |
| Sum | 162,761 | 174,436 | 93.811 | 102.146 |

Tokens are input including cache plus output. Skill costs **7.2% more tokens /
8.9% more time** in aggregate. It is slightly faster on the compatible control,
but not cheaper in tokens. One sample and unequal work do not establish causal
effects. Do not promote this as an efficiency result.

## Actual evidence and decisions

All four read the deployed producer and worker from HEAD~1 and execute the actual
functions, rather than assuming current worker code represents deployed code.
Neither skill invocation reads the SQLite reference or uses that helper for this
non-SQL contract. Conditional history routing did not suppress needed history.

In the incompatible case, both execute four producer/worker pairings for seven
nonempty titles, identify new-only title payloads failing on old name-only workers,
and reproduce retained candidate jobs failing after worker rollback. Both explain
why restoring old producers does not convert queued payloads and keep operational
readiness unverified. Skill also enumerates six rollout/rollback states; baseline
uses the pair matrix and a retained-job rollback check. Original command counts
are six skill versus four baseline, including extra inventory/metadata steps.

In the compatible case, both correctly find no payload blocker: the deployed
worker already handles either key, like the candidate. Neither demands unnecessary
draining or conversion for this contract; both distinguish payload compatibility
from unverified staging/queue operations. Baseline runs 32 pair checks and 39
retained-backlog deliveries (71 reported equality checks). Skill runs 28 pair
checks and 364 state/rollback deliveries, mapping rollback from each rollout
state. Both use four shell commands, so call count alone does not explain cost.

The fixture functions have no state beyond the supplied dictionary/string. Many
of skill's phase-labeled deliveries repeat the same worker with equal payloads;
phase names do not change those function inputs. This is a concrete opportunity
to reuse established pair evidence while still reasoning about every reachable
state. It does not justify collapsing stateful application writers, transactional
effects or changed data into an old result. More assertion invocations are not
automatically broader distinct behavior coverage.

## Integrity and next action

All four complete without timeout, rejected patch or capture diagnostic flags.
All sixteen original file instances match fixture bytes; diffs are empty. All
eight installed resource instances match frozen Git blobs and before/after
inventories. Commands and original behavioral outputs were inspected within
project scope. No deployment, install, external service or original-file edits.
Clean snapshots and diagnostics do not establish all transient behavior or full
capture. Author fixture checks are separate from original model execution.

Retain the correct history-dependent decisions and adverse costs. The next
candidate should distinguish unique compatibility evidence from repeated labels
of the same state-independent pairing, preserving new data and genuinely distinct
state transitions. Do not rerun this pair for a favorable score or generalize its
stateless contract to production systems. The full performance objective remains
unmet.
