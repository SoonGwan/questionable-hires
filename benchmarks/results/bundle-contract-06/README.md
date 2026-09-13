# Whole-bundle development checkpoint 06

Resource/launch `20ec916`; nine exposed synthetic tasks, all eight skills,
18 fresh serial GPT-6 Astra medium sessions, n=1. All completed; no exclusions
or timeouts. Not a held-out confirmation or real-project generalization.

| Arm | Input + output tokens | Summed process seconds |
| --- | ---: | ---: |
| Baseline | 713,178 | 511.591 |
| Skill | 686,327 | 418.570 |
| Skill change | −3.76% | −18.18% |

Five task pairs cost more with skill. Unequal additional checks/artifacts, shared
host/cache and the persistence baseline's incomplete native output limit these
descriptive ratios of sums. Cached input is counted once. No broad 20–30% gain,
causal attribution or release readiness claim; featured results are unchanged.

- [Frozen protocol](../../BUNDLE-CONTRACT-06-PROTOCOL.md)
- [Every pair, limitations and final review](../../BUNDLE-CONTRACT-06-REVIEW.md)
- [All scheduled cells](run.json) and [metadata](summary.json)
- [Separate post-timing reconciliation and 12 controls](author-replay.json)
  from [replay code](../../replay_bundle_contract_06.py)

All 18 original event streams, usage and resource hashes reconcile. All 12 author
checks match, including transient-fault rejection and valid-correction acceptance;
retained projects are unchanged. Replay never replaces missing original output.
Cell directories preserve redacted events/commands, answers, diffs, final projects
and original source hashes. Original measurements remain immutable.
