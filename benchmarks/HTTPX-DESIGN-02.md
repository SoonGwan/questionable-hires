# Resolve real paths: targeted follow-up

One fresh skill execution at `925758f` on the unchanged transport design task,
same pinned HTTPX/design environment, Astra medium. No baseline rerun or retry.
Local evidence: ignored `local-runs/httpx-design-02`.

| Sample | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| Previous skill | 194,663 | 86.177 |
| Current skill | 152,636 | 78.438 |
| Earlier baseline | 148,202 | 85.133 |

Current versus previous skill: 21.6% fewer tokens, 9.0% less time. Versus earlier
baseline: 3.0% more tokens, 7.9% less time. These separated single samples do not
establish a causal or repeatable efficiency win. Test selections differ: current
executes 12 lifecycle/state tests, previous skill 15 focused tests, baseline 19.
Do not hide verification-depth differences behind percentage improvements.

The current trace uses discovered paths, has no repeated nonexistent-path reads
and stays within the explicit project boundary. It retains the supported sync/
async extension and lifecycle contracts, buffering and handler dispatch, Python
support constraints, and the stale docstring finding. It does not merely skip
the requested design review. In-memory probes additionally exercise synchronous
streaming bodies and the three asynchronous handler forms, plus sync rejection.

The probe command's captured aggregated output is empty despite recorded exit 0.
The author therefore independently replayed that exact retained command in the
final project copy: exit 0, explicit handler/body pass output and the expected
tuple-URL TypeError / missing stream.read evidence. The model trace alone is not
credited as a captured probe-output chain. The pytest trace records 12 passes.

Provenance audit matches all 125 original files, source revision and the two
frozen/installed Landlord resource hashes. No source edits or patch rejections.
This supports a targeted correction and complete task criteria in this sample,
not all-skill superiority or proof across supported Python versions. Retain the
candidate and verify transfer on a different meaningful task before more tuning;
do not rerun this unchanged review hoping to beat baseline tokens.
