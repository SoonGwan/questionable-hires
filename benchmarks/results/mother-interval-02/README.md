# Native QA work-selection checkpoint 02

Resource/launch `160ff71`; two unchanged exposed authored tasks, four fresh serial
Astra medium cells at n=1. All completed, no timeouts/exclusions.

| Arm | Recorded input + output tokens | Process seconds |
| --- | ---: | ---: |
| Baseline | 167,864 | 119.365 |
| Skill | 143,459 | 219.063 |

**−14.54% tokens / +83.52% time**; not an overall efficiency win. Skill avoids
repeat-key/assertion-library extras while retaining required assertions in source
and separate unchanged-test replay. One skill cell records connection resets;
another has no original native test output. Do not reconstruct either as clean
model evidence or subtract presumed reconnect delays.

Initial author replay misses nested tests (zero discovered, marked unmatched).
An explicit discovery directory then exercises all eight expected controls. Both
records remain; generated tests and originals are unchanged. Author replay cannot
replace absent model output. Two exposed tasks, n=1 and unequal work prevent broad
claims. Historic and featured graphs remain unchanged.

- [Protocol](../../MOTHER-INTERVAL-02-PROTOCOL.md), [review](../../MOTHER-INTERVAL-02-REVIEW.md)
- [Schedule](run.json), [metadata](summary.json)
- [Initial author replay](author-replay.json), [explicit discovery](author-replay-explicit-discovery.json)
- [Replay utility](../../replay_mother_interval_01.py)
