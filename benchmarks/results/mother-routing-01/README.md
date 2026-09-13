# Delivery-route checkpoint 01 — improvement not accepted

Resource/launch `672e22f`, two exposed authored tasks, four fresh serial Astra
medium sessions, one repeat per arm. All complete, no timeouts/exclusions.

| Arm | Total tokens | Process seconds |
| --- | ---: | ---: |
| Baseline | 149,888 | 151.985 |
| Skill | 161,752 | 116.490 |

Aggregate **+7.92% tokens / −23.35% time**. Observation pair: +4.38% / −57.33%;
native-test pair: +10.72% / +15.01%. The skill selects the intended document route
but does not reduce aggregate tokens. Different extra checks, n=1 and shared host/
cache preclude causal conclusions or general/all-eight claims.

Both report no defect on the original clean components. Separate unchanged-test
author replay verifies standalone execution and exposes a coverage gap: baseline
tests reject a transient intermediate-display fault; skill tests merely print it
and pass. Do not equate successful route selection or green tests with robust QA.

- [Protocol](../../MOTHER-ROUTING-01-PROTOCOL.md)
- [Native review and limitations](../../MOTHER-ROUTING-01-REVIEW.md)
- [Schedule](run.json), [all metadata](summary.json)
- [Separate author replay](author-replay.json), [replay code](../../replay_mother_routing_01.py)

Each cell retains redacted full commands/events, answer, final project, metadata,
diffs and raw-file provenance hashes. Replay never replaces native model evidence.
Historical and featured charts are unchanged.
