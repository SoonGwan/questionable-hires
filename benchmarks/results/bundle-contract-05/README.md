# Whole-bundle development checkpoint 05

Resource `d4a52ef`, launch `3bf7752`; nine exposed synthetic tasks, eight skills,
18 fresh serial GPT-6 Astra medium sessions, one repeat per arm. All completed;
zero timeouts/exclusions. This is development evidence, not a held-out confirmation.

| Arm | Input + output tokens | Summed process seconds |
| --- | ---: | ---: |
| Baseline | 748,007 | 523.202 |
| Skill | 724,706 | 478.555 |
| Skill change | −3.12% | −8.53% |

Cached input is counted once. Different additional checks/artifacts and shared
cache/host limit interpretation. One skill QA cell has missing native test
output; its later author replay cannot fill the original capture gap. These
ratios of sums are not the historic chart's equal-task mean ratios. No broad
20–30% improvement, universal superiority, or public-release readiness is claimed.

- [Frozen protocol](../../BUNDLE-CONTRACT-05-PROTOCOL.md)
- [Per-pair review, adverse findings and reconciliation](../../BUNDLE-CONTRACT-05-REVIEW.md)
- [All scheduled cells](run.json) and [raw metadata summary](summary.json)
- [Separate post-timing author replay](author-replay.json), produced by
  [unchanged-test replay code](../../replay_bundle_contract_05.py)

Each cell directory retains redacted events/commands, final answer, metadata,
diffs, source hashes and final project files. Installed resources are identified
by per-file hashes and measured Git revision, not duplicated as project consumers.
Source hashes describe private raw originals; exported text redacts local paths.
All original experiments remain unchanged.
