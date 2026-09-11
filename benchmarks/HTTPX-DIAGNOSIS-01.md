# HTTPX diagnosis: boundary localization and remaining overhead

Followed the committed [plan](HTTPX-DIAGNOSIS-PLAN.md): one redirect-auth task,
one baseline/current-skill pair, then one evidence-driven skill correction.
All use pinned HTTPX, the design environment, Astra medium and fresh serial
sessions. Ignored raw evidence: `local-runs/httpx-diagnosis-01` and
`local-runs/httpx-diagnosis-02`. These are exposed author-selected development
samples, not held-out incident data or repeatability evidence.

| Sample | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| Baseline | 141,113 | 102.407 |
| Prior Exorcist, snapshot `3ff38dd` | 102,462 | 66.826 |
| Boundary-instrumentation revision `30eb9b5` | 116,639 | 62.584 |

The first skill uses 27.4% fewer tokens and 34.7% less time than this baseline.
The correction is **13.8% more tokens**, 6.3% less time than the first skill;
versus baseline it is 17.3% fewer tokens and 38.9% less time. Do not select only
the favorable comparison. Baseline records a rejected patch before successfully
creating its local reproduction; its attempted rejected target is not captured
in sufficient detail to assign intent. This retry and verification differences
confound causal speed/token claims.

## Actual behavior

All three run original HTTPX with a recording MockTransport and dummy credential,
assert source-import provenance, block socket/DNS use, and exercise the reported
8443 redirect, default-HTTPS redirect and same-origin control. Captured outputs
show removal/preservation/preservation respectively. They trace effective
scheme/host/port comparison and the same-host 80-to-443 exception to actual
redirect construction. All distinguish the cache-free local reproduction from
unknown production behavior and recommend trusted-destination handling without
unconditionally forwarding credentials. All frozen task criteria are supported.

The original skill additionally tests a cross-host protection control. It wraps
`_build_redirect_request` in a subclass to record the same header again before
the recording transport sees it, and reports private helper predicates. Baseline
instead repeats all three cases without following redirects to inspect the public
`next_request` object. Neither extra observation is credited as a task requirement.

The revision prefers existing observation points over private wrapping when the
upstream transformation and downstream input already localize the symptom. The
follow-up preserves the three required controls without subclasses/private helper
imports, and derives the transformation from source plus transport inputs. It
does not execute the extra cross-host control. That coverage difference remains
explicit; simpler instrumentation alone is not evidence of all-skill performance.

Both skills still read pytest configuration/fixtures despite running a standalone
probe, and the follow-up splits discovery/reads into more shell calls. This is a
remaining efficiency opportunity, not grounds to silently disregard setup that
could affect a different diagnosis. The revision successfully changes observer
selection in this sample but does not improve both cost measures over prior skill.

## Integrity and next gate

Provenance audit verifies all 125 original files unchanged in all three final
snapshots, pinned upstream revision, and both installed/frozen Exorcist resources.
Full command/artifact review finds in-project successful writes only to retained
diagnostic files, no source implementation or credential-protection changes, and
no network execution. The rejected baseline patch remains a provenance limitation,
not a confirmed external write. Final snapshots alone cannot prove absence of
transient/outside effects.

Local package tests: 89 passing; validation covers eight skill metadata/link
sets. Relevant upstream preflight: two passes before each run. These are not
model success scores. The new diagnosis profile preserves the historical audit
profile and its defaults; no previous results were overwritten or reclassified.

Keep the boundary-instrumentation change a targeted candidate. Before broad
acceptance, test a distinct diagnosis where a single boundary does leave the
origin ambiguous, plus the fixed nine-task regression screen. Do not force early
stopping or repeat this unchanged report to chase the lower baseline number.
