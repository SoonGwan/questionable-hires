# Interval-contract checkpoint 01

Resource/launch `14289df`, two unchanged exposed authored tasks, four fresh serial
Astra medium cells at one repeat. All complete; no timeouts/exclusions.

| Arm | Input + output tokens | Process seconds |
| --- | ---: | ---: |
| Baseline | 150,718 | 135.818 |
| Skill | 164,758 | 150.187 |

Aggregate **+9.32% tokens / +10.58% time**. Efficiency target unmet. The new rule
is adopted: protected native skill tests assert intermediate retention, while
final-only tests leave permitted intermediate display unconstrained. Separate
unchanged-test replay rejects the previous transient fault and accepts the valid
guarded correction for both arms.

Both skill executions have partial native output: summaries and targeted evidence
are captured, but earlier per-test lines are absent. Author replay cannot fill
those original gaps. Unequal extra checks/artifacts, shared host/cache and n=1
preclude causal or broad claims. Earlier routing failure remains preserved.

- [Frozen protocol](../../MOTHER-INTERVAL-01-PROTOCOL.md)
- [Per-cell review and limits](../../MOTHER-INTERVAL-01-REVIEW.md)
- [Schedule](run.json), [all metadata](summary.json)
- [Separate author replay](author-replay.json), [code](../../replay_mother_interval_01.py)

Each cell retains full redacted captured events/commands, final project/answer,
diffs, metadata and raw-file provenance hashes. No test or measured fixture was
rewritten to improve the result. Featured and historic charts are unchanged.
