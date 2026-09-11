# Conditional setup reading: behavior changes, cost still regresses

Candidate `a060148`, following the committed [plan](EXORCIST-RUNNER-PLAN.md).
Two fresh skill-only Astra-medium sessions, serial, two tasks; no retries or
baseline rerun. Raw evidence remains in ignored `local-runs/httpx-diagnosis-03`
and `local-runs/exorcist-runtime-01`.

| HTTPX redirect diagnosis sample | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| Earlier baseline | 141,113 | 102.407 |
| Original skill sample `3ff38dd` | 102,462 | 66.826 |
| Boundary observer revision `30eb9b5` | 116,639 | 62.584 |
| Execution-path revision `a060148` | 139,927 | 95.090 |

The latest sample costs about 20.0% more tokens and 51.9% more time than the
preceding skill. It is not an efficiency improvement. It also records a rejected
patch before successful artifact creation, as the earlier baseline did. The
rejected target is not sufficiently captured to attribute the cause or intent.
Keep this operational confound and all raw costs; do not discard the sample or
claim either that the instruction caused the whole regression or that removing
the retry would necessarily produce a win.

The requested behavior change is observable: no pytest configuration/conftest
reads, no private observer subclass, and a recording MockTransport verifies the
same three required actual-request cases. Origin/port and upgrade-exception
reasoning, safe destination advice and original-file preservation remain intact.
Unlike the preceding probe, it does not install a socket-denial guard, but uses
only the inspected local MockTransport path with `trust_env=False`; no network
call is observed. Local evidence does not certify deployment behavior.

## Configuration-is-relevant control

`runner-environment-timing` uses 69,483 tokens and 53.601 seconds. There is no
baseline for this new authored fixture and no comparative efficiency claim.

The model reads the actual worker and unittest setup, then retains a harness
which executes fresh subprocesses for the original failure, actual setup versus
effective module policy, pre-import environment control and unchanged unittest
under startup configuration. It correctly observes environment `'0'` alongside
module `RETRIES=2`, three callback invocations, and one callback when configured
before import. It recommends matching startup semantics without inventing a
requirement for live configuration changes or an intermittent external cache.

The command's captured output omits the first subprocess's original-failure
section, although its retained script includes and checks that subprocess. The
author independently replayed the exact retained script after all model runs:
explicit `AssertionError: 3 != 1`, followed by the actual setup observations,
standalone one-callback result and unchanged unittest passing. Original capture
alone is not credited as the full failure-output chain. Fresh subprocesses are
not time-bounded in the authored probe; this is finite fixture evidence, not a
general-purpose hardened diagnostic runner.

## Verification and disposition

HTTPX provenance checks confirm all 125 original files, source revision and both
frozen/installed skill files. Control checks confirm all three original fixture
files and both installed skill resources. Successful diagnostic writes stay
inside their projects; no production edits or installations. The control's file
discovery unnecessarily lists `.git` paths but does not leave the project.
Final snapshots and successful command review cannot resolve the rejected patch
target or prove absence of every transient effect.

Full local suite: 90 tests passed, including fresh-process fixture validation.
All eight metadata/link sets and Exorcist skill validation pass. Character,
description and invocation metadata are unchanged. No full-team regression screen
has run at this snapshot and broad performance improvement remains unproven.

Keep the change experimental: it avoids irrelevant setup while retaining relevant
setup in these samples, but does not meet the resource objective. Investigate the
recurrent artifact-creation/capture confounds before another token-optimization
claim; do not keep accumulating rules or resampling this unchanged redirect task.
