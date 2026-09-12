# Condensed interaction and rollout reviews

Candidate `b347792` removes repeated workflow/delivery guidance from Mother-in-law and Friday while preserving deterministic sequence controls, effect-layer limits, actual rollout/rollback states, new-data recovery, explicit scope and stopping conditions. These are candidates, not proven efficiency upgrades.

Three unchanged development cases, one fresh skill-only sample each, Astra medium, serial. Local evidence: `local-runs/fast-state-reviews-01`. All completed without timeout. The author inspected answers, commands and fixture preservation; all three fixed task criteria sets were met. No baseline was run in this screen.

| Case | Earlier skill tokens / seconds | Candidate tokens / seconds |
| --- | --- | --- |
| search-order | 85,325 / 50.411 | 68,534 / 47.325 |
| search-protected | 67,761 / 40.576 | 84,724 / 42.579 |
| rolling-schema | 67,648 / 39.488 | 67,627 / 34.481 |

Earlier samples are from `fast-regression-01`; comparisons are temporally separated single observations, not causal estimates. Tokens include cached input once plus output. Efficiency is mixed: the protected-search sample uses substantially more tokens, the failing-search sample fewer, and rollout-review tokens are essentially unchanged. Do not describe these changes as an across-the-board performance gain or select only the favorable task.

For failing search, controlled reverse completion fails the latest-result assertion while the normal-order control passes. Protected search tests both completion orders and correctly reports no stale overwrite. Both use the actual state implementation and leave production files unchanged, explicitly limiting claims to state rather than browser rendering. Friday executes actual migration/query combinations locally, identifies both rollout and rollback incompatibility, checks representative post-upgrade data through reversal, and leaves the untested deployment unknown rather than safe. All fixture input files are unchanged; QA adds only reproduction tests.

Remaining overhead includes repeated directory/status discovery. The protected-search run also chains its test with later commands; its passing output is visible, but the overall shell exit alone would not prove the test passed. Do not prescribe more universal rituals from this single observation. Broader interaction paths, actual browser behavior and non-rolling deployments remain untested by this screen.
