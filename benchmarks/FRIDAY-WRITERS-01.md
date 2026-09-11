# Mixed writers: useful findings, no overall efficiency gain

Protocol and two synthetic fixtures were committed at `6c3d89c` before execution.
Astra medium, baseline and explicit Friday, one repeat each, serial seed 20260911.
Order: control skill, gap skill, gap baseline, control baseline. No retries,
timeouts or exclusions. Local ignored evidence: `local-runs/friday-writers-01`.
Friday entrypoint `4ac4ffe`, helper/reference `e79b208`; no skill edits during run.

| Case | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| Writer gap | 80,937 / 47.410 | 70,811 / 53.713 |
| Synchronized control | 85,302 / 79.558 | 108,923 / 79.235 |
| Total | 166,239 / 126.968 | 179,734 / 132.948 |

Tokens include cached input plus output. Total skill costs +8.1% tokens / +4.7%
time. Gap tokens fall 12.5% while time rises 13.3%. These single shared-host
observations with different verification depth are not causal performance estimates.

## Actual execution

Both gap arms execute the supplied functions and migrations. They demonstrate
stale reads across each writer direction, old inserts producing null new values,
and acknowledged new updates lost after down. Both include new-insert then update
and retain ordinary successful operations. Friday additionally executes opposite
writer orders to show that blind column copying cannot identify the latest write.

Both control arms recognize compatibility after completed migration and data
retention after down. Baseline's original captured output reports 508 scenarios,
8,720 committed writes and 52,320 read assertions: writer sequences of lengths
0–6, recursive-trigger combinations, integer boundaries, aborted writes and
post-rollback old operations. These are local check counts, not production coverage.

Friday also checks integer boundaries, recursive triggers and seven operation
prefixes through rollback. It investigates a further boundary: old writes between
backfill and trigger creation. Original execution output shows separate local
connections producing stale/null fields without an enclosing transaction, and
blocking then synchronized values with an atomic migration. It therefore reports
ready with a migration-execution prerequisite, not that completed coexistence fails.

The original protocol specified coexistence after migration; runner transaction
semantics were not supplied. Keep this extra finding separate from the frozen
post-migration criteria. Do not retroactively fail the baseline or redefine the
compatible control to make Friday win. Neither model establishes production or
restore readiness. SQLite shared-memory checks do not model production locking.

Friday reads the optional matrix reference in both cells but does not use the
helper, appropriately executing real writer functions instead. It performs five
shell commands on the gap and six on the control; baseline performs five and
four respectively. Unused reference loading and repeated status/history inspection
are candidates for overhead reduction, not a proven token-cost decomposition.

## Integrity and next action

Original command traces and outputs were inspected. All five fixture files in
each cell remain byte-identical. Installed Friday resources match committed blobs
and before/after manifests. No patch rejections or capture flags; empty flags and
final hashes cannot certify all transient behavior or output completeness. No
separate author replay is represented as model evidence.

The fixed local behaviors are demonstrated, but scope and verification depth
differ. Preserve the adverse aggregate. A subsequent candidate should target
contract-relevant transitions and avoid loading reader-only machinery for actual
writer execution; do not mandate a large state enumeration or suppress a material
migration prerequisite merely to improve speed. No broad completion claim.
