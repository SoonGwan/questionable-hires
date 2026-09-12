# Required provenance survives; efficiency remains adverse

Snapshot/protocol 1371ebb, entrypoint 4a2eeb7, runner fd8d578. One new invoice
provenance task, fresh Astra medium baseline then skill, serial, one repeat each,
seed 20260911, 240-second limit. No retries or exclusions. Original private logs
are retained in `local-runs/exorcist-provenance-01/`.

| Arm | Input + output tokens | Process seconds | Shell commands |
| --- | ---: | ---: | ---: |
| baseline | 67,541 | 88.847 | 3 |
| skill | 114,116 | 106.930 | 7 |

Skill costs **69.0% more tokens / 20.4% more time**. Cached input is already
included. Shared host, one pair and unequal work prevent causal/general claims.

Both exercise actual worker.handle and Invoices.get, reproduce the shared-ID
cross-tenant overwrite with one dispatch per request, reverse the request order,
and demonstrate normal distinct-ID behavior. Baseline additionally checks fresh
instances and repeated same-tenant requests (five scenarios versus skill's three).
Both correctly distinguish this local cache-key failure from unknown production
queue behavior. Both retain a rerunnable probe, machine-readable provenance and
an explanatory document. Required traces are not waste merely because retained.

Author inspection of original probe execution and retained JSON confirms source
read references resolve to the returned text. Skill also links reads during each
request to its request identity. Both use unique fixture text to disambiguate the
observed source; neither claims this method proves arbitrary production provenance.
All three original files per arm remain byte-identical to the frozen fixture.

Skill directly consumes helper stdout and does not reread a result file, but its
probe both saves the required trace and prints the full trace, nested into helper
JSON. Baseline saves its trace and emits compact per-scenario counts. Thus required
artifact retention succeeds; compact console evidence is not adopted. Skill also
invokes the process wrapper on bounded synchronous dictionary operations with a
local recording callback: the inspected path has no uncertain asynchronous wait,
blocking external I/O or cancellation suppression to justify that extra mechanism.
This motivates reconsidering helper routing, not another universal logging rule.

Skill's initial `rg` search for absent AGENTS.md exits 1 and short-circuits its
chained skill read. It then performs separate listing, skill read, status and input
read commands. The initial failed command precedes loading this candidate and
cannot be attributed to its body. No external/scope-expanding commands are captured.
Neither arm has capture flags, patch rejections, timeouts or event errors. Four
installed resource hashes match the frozen Git snapshot and before/after manifests.
Baseline groups execution and final Git checks with semicolons, so the aggregate
exit alone does not establish probe status; captured final assertion-success output
and inspected probe establish execution evidence. No author replay is credited.

The new author fixture test and all 155 repository tests pass (16.961 seconds);
repository validation passes. These are not end-to-end performance evidence.
No skill edits followed this run. Do not repeat this exposed case to chase a win.
