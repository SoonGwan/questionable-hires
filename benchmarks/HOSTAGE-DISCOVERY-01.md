# Scoped discovery regression: no efficiency win

Protocol HOSTAGE-DISCOVERY-PROTOCOL.md, frozen snapshot e985e3e, entrypoint
91c33c8. Original serial runner completed both fresh sessions, exit 0; no retries
or exclusions. Raw records remain in ignored local-runs/hostage-discovery-01.

| Arm | Input + output tokens | Process seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 80,561 | 45.585 | 4 |
| Skill | 105,775 | 47.746 | 6 |

Skill costs +31.30% tokens / +4.74% time. This exposed single pair does not establish
causality, generalization or whole-bundle benefit. Cached input is not added twice.

Both arms read upload.py and test_upload.py together, then requirements separately.
The candidate does not demonstrate the intended combined discovery/read behavior.
Its first listing occurs before loading the body. After loading, it lists again,
reads implementation/tests, then batches `cat requirements.md; python -m unittest
-v`. The file explicitly specifies python3 -B, but the already-issued command uses
unavailable python and exits 127. A corrected command captures the original failure
and the final suite captures all four passes. Baseline runs only the final suite.
Thus the extra cost includes actual before evidence and a preventable command
failure, not just skill text or test depth. Reading instructions and executing a
command that depends on their contents in the same tool call loses that dependency.

Production fixes are byte-identical: per-instance duplicate guard plus try/finally,
preserving client return values and exceptions. Both extend existing unittest tests
with overlap and cancellation/retry coverage. Original test method ASTs match;
requirements and branding match bytes. Two installed skill resources match frozen
Git SHA-256 and before/after manifests. Recorded commands stay inside each project;
metadata reports no empty outputs, malformed JSON, rejected patches or event errors.
Those flags do not prove complete capture.

Skill shares an in-flight test helper across normal/cancel paths and bounds behavior-
dependent waits. Baseline repeats two unbounded controlled sequences. Neither adds
a parallel framework. No rendered UI is supplied or independently tested.

## Separate author fault check, not model execution

After both timed sessions ended, the existing con-artist audit.py and
hostage-duplicate-audit.json ran against each retained project with timeout 3.
The helper verifies copied imports and removes only the exact duplicate guard in
isolated copies. Both correct suites pass. Skill mutant reports two local
asyncio.TimeoutError failures at the duplicate call, completes all four tests in
2.073 seconds, exit 1, without process timeout. Baseline mutant stalls in overlap
until the three-second process timeout (exit -9); audit status is incomplete.
The displayed skill audit output was tool-output truncated, while its returned
check statuses and ending traceback/summary were visible. No absent output is
reconstructed or counted as model evidence.

This supports bounded detection of this particular removed guard, not termination
under every async fault. Preserve the useful bounded tests. Discovery consolidation
alone did not deliver savings; do not respond by stripping verification or repeatedly
sampling this case. Next investigate dependency-aware command selection rather than
merely demanding fewer tool calls. No new candidate change accompanies this result.
