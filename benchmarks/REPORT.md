# Astra smoke evaluation — 2026-09-10

Eight hires were exercised on real Codex sessions, with actual file inspection and command execution. The main matrix contains **24 runs: eight tasks × three arms × one repetition**. A separate set contains **eight skill-only clean, limiting, or necessary-change cases**. An earlier three-run eligibility pilot is retained separately and excluded from the main matrix.

**The central findings were usually the same without a skill.** These runs demonstrate that the workflows can function on these synthetic examples; they do not demonstrate statistical superiority, general reliability, lower cost, or production readiness.

## Setup and evidence

- Model: `gpt-6-astra`; reasoning setting: `medium`.
- Host: Codex CLI `0.153.4`, authenticated through ChatGPT.
- Three concurrent independent processes; fresh synthetic Git repositories with identical initial commits per task.
- Arms: no project skill, a short generic instruction, or the corresponding installed and explicitly invoked skill.
- User configuration ignored; nine discovered personal skills disabled. Built-in runtime instructions remain. No unrelated skill loading was observed in the reviewed command records, but this is not a proof of complete system-prompt isolation.
- Scope: local synthetic code, no external service calls, no deployments.
- Scoring: author review of final answers, actual command output, source snapshots, and diffs against the predefined case criteria. This is not a blinded third-party review.

Inspect the [main run manifest](results/astra-2026-09-10/run.json), [per-cell metadata](results/astra-2026-09-10/summary.json), [clean run metadata](results/astra-clean-2026-09-10/summary.json), and [pilot](results/pilot-2026-09-10/run.json). Each cell includes an answer, command/output record, diff, and final source snapshot. Local path prefixes have been replaced for sharing; commands containing those placeholders need corresponding local paths when rerun.

## What changed between arms?

| Task | No skill | Short instruction | Corresponding hire |
| --- | --- | --- | --- |
| Legacy fallback | Kept active v1 compatibility; cited current consumer | Also cited introducing commit | Connected both historical commits to current support contract |
| Age boundary | Fixed boundary with failing-before regression | Same correct fix and regression | Same fix; explicit revision, command, and verification limits |
| Formatter registry | Recommended plain USD function | Same; tested proposed equivalence extensively | Same; explicitly retained useful module boundary |
| Search interaction | One deterministic stale-result reproduction | Same reproduction, repeated ten times | Two failing reproductions plus a passing order control; noted no browser exercised |
| Cache suspicion | Demonstrated response ordering without cache | Same causal finding | Same; suggested generation guard and bounded local conclusion |
| Button label | Exact requested change only | Exact requested change only | Exact requested change only |
| Lost-write test | Demonstrated surviving mutation; originals unchanged | Found survivor and also changed existing test | Demonstrated survivor and stronger assertion in disposable copy; originals unchanged |
| Rolling schema | Identified both incompatible reader windows | Same blockers and missing staging evidence | Same; additionally distinguished SQLite demonstration from unknown runtime compatibility |

The control arm's existing-test edit during an audit is a scope-review caution, not evidence that it produced a wrong implementation. It illustrates why correctness and scope should be inspected separately. The skill's longer output or extra test does not automatically constitute a better result.

Independent snapshot checks confirmed the age boundary behavior for 17/18/19 in all arms and the exact label-only change in all arms. Original production files remained unchanged in the investigation tasks. The detailed [examples](../examples/README.md) link to all three answers for each task.

## Time observations, not speed claims

Elapsed wall seconds, one sample per cell. Runs shared a machine and account; caching, queueing, and concurrency affect these observations.

| Task | No skill | Short instruction | Skill |
| --- | ---: | ---: | ---: |
| Legacy fallback | 30.015 | 30.062 | 31.267 |
| Age boundary | 34.540 | 39.844 | 44.699 |
| Formatter registry | 24.242 | 32.842 | 24.000 |
| Search interaction | 41.027 | 54.710 | 56.292 |
| Cache suspicion | 47.385 | 52.661 | 49.438 |
| Button label | 22.588 | 27.404 | 27.185 |
| Lost-write test | 40.357 | 45.066 | 47.969 |
| Rolling schema | 37.250 | 39.565 | 37.230 |

Skills were often slower in this run. No speed or cost improvement is claimed. Reported token usage is preserved per cell, including cached input; it is not converted into dollars. Different amounts of cached context and accumulated tool-loop input make raw token totals unsuitable as a standalone quality metric.

## Can the hires leave good code alone?

The separate skill-only cases showed the expected central behaviors:

| Hire | Case | Observed outcome |
| --- | --- | --- |
| Necromancer | Historical consumer retired | Allowed removing the obsolete fallback under the current contract |
| Receipt | Only fixed snapshot available | Verified current boundaries and explicitly marked before evidence unavailable |
| Landlord | Single-consumer compatibility adapter | Recommended keeping the justified boundary |
| Mother-in-law | Generation-protected search | Reported no reproduced overwrite after controlled tests |
| Exorcist | Remote failure without runtime evidence | Declined to assert a root cause; identified the missing observations |
| Hostage Negotiator | Pending state genuinely required | Implemented pending, duplicate prevention, and reset on success/failure |
| Con Artist | Existing persistence assertion effective | Showed the mutation is killed; no needless stronger assertion |
| Friday | Additive nullable schema change | Found no evidenced compatibility blocker; kept staging readiness unknown |

These eight cases have no baseline/control repetitions, so they support only a limited behavioral smoke check, not a comparison.

## Automatic routing with the whole team

Eight further sessions installed all eight hires and supplied the task without naming a skill. The expected skill file was read in all eight observed sessions. The eligibility task also selected Hostage Negotiator alongside Receipt; selection need not be exclusive.

See [routing answers and command evidence](results/astra-routing-2026-09-10/summary.json). This is one task per expected hire, not a measured false-positive rate or a guarantee of future routing. The first routing pilot installed only one hire and used ambiguous wording about other installed skills. Its [eight records](results/routing-pilot-2026-09-10/summary.json) are retained but excluded from the whole-team routing conclusion.

Local plugin installation was separately checked through a real CLI install/list/cache-comparison/remove cycle. See the [installation record](../docs/INSTALLATION-TEST.md).

## What remains unproven

- Repeatability across independent samples, harder tasks, larger repositories, languages, and tool environments.
- Routing repeatability and false positives across broader unrelated requests.
- Actual browser interactions: search cases exercise Python state boundaries, not a rendered UI.
- Production database behavior or deployed rollback procedures.
- Remote Git marketplace installation, public directory submission, and other hosts.
- Complete absence of hidden runtime context contamination.

Reproduce the main suite with the commands in [the runner guide](README.md). To run the additional skill-only cases:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/clean --suite clean --arms skill --jobs 3
```

Future performance claims need repeated trials and broader tasks. Keep ties, failures, and regressions in the report. A memorable character earns its place through useful behavior, not a flattering chart.
