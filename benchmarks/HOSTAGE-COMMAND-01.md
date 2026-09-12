# Command transfer: correct invocation, no cost advantage

Frozen protocol af8050e, candidate 1afcc46; original serial runner completed both
sessions with exit 0, no retries/exclusions. Raw records are in ignored
local-runs/hostage-command-01. This is one authored transfer pair, not independent
held-out confirmation or a causal efficiency measurement.

| Arm | Input + output tokens | Process seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 63,194 | 24.694 | 3 |
| Skill | 86,404 | 34.317 | 7 |

Skill costs +36.73% tokens / +38.97% time. Cached input is included once.

Both read README, implementation and checks together, then use the documented
python3 discovery invocation in a later call. Neither guesses an unavailable
interpreter nor executes the empty default suite. Both produce byte-identical
production/test changes: <= becomes < and exact-limit plus zero-limit assertions
extend the existing suite. Original test ASTs, README and branding are preserved.
Signature and permanent-failure branch are unchanged. All five final tests are
actually captured as passing; no external service or dependency setup occurs.

Baseline discovers twice, reads once, then executes the final suite. Skill discovers,
loads its entrypoint separately, reads the three relevant files together, performs
another hidden-file listing, executes the new regressions before the fix (two exact
assertion failures captured), checks the focused diff, then executes the final suite.
The additional before evidence is real but not a newly imposed task criterion.
The later listing and separate entrypoint/diff calls also contribute work; costs
must not be attributed entirely to test depth. Seven calls do not imply seven
unnecessary calls, and three calls alone do not establish equivalent evidence.

Both resource manifests are unchanged; the skill's two installed files match frozen
Git SHA-256. Original metadata reports no empty-output flags, malformed/non-object
JSON, event errors or rejected patches. This does not prove exhaustive capture.
No author replay is credited as model execution.

The dependency-aware behavior is observed in both arms, so it cannot establish a
skill-induced improvement. Avoid another wording rule or rerun merely because this
pair is adverse. The candidate remains unproven for the broad efficiency objective;
the next useful direction is reducing actual first-load/workflow overhead without
discarding necessary verification, not tuning this particular boundary exercise.
