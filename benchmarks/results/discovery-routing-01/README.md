# Discovery routing 01 — adverse/incomplete development screen

Skill resource `07fa9e2`; atomic launch `3cbcd3e`, Store launch `a74f95c`
(intervening documentation only). Two unchanged exposed authored tasks, fresh
baseline/skill sessions, n=1, serial Astra medium, 240s/cell. Not holdout evidence.

| Task/arm | Tokens | Seconds | Completion |
| --- | ---: | ---: | --- |
| Atomic baseline | 83,380 | 49.277 | Complete |
| Atomic skill | 89,568 | 87.526 | Complete |
| Store baseline | 65,155 | 83.303 | Complete |
| Store skill | Unknown | 240.027 | Timeout after connection reset |

Atomic skill records +7.42% tokens and +77.62% time, with additional exception
coverage. No aggregate token ratio, retry, exclusion or inferred timeout-cause
claim. Unknown usage is not zero; intermediate native checks do not constitute
a delivered Store review. Efficiency improvement remains unproven.

- [Frozen protocol](../../DISCOVERY-ROUTING-01-PROTOCOL.md)
- [All cell reviews and limitations](../../DISCOVERY-ROUTING-01-REVIEW.md)
- [Atomic metadata](atomic/summary.json) and [Store metadata](store/summary.json)
- [Separate reconciliation and four native replays](author-replay.json), using
  [author replay code](../../replay_discovery_routing_01.py)

Raw streams/resources reconcile including the incomplete cell; all four author
before/after controls match with unchanged retained tests and preserved original
methods. Reproduced verbose subtest formatting explains the atomic header warning;
it does not resolve unrelated capture gaps. Original model attempts are immutable.
Featured charts stay unchanged. Exported paths are redacted; source hashes identify
the private originals, not the redacted copies.
