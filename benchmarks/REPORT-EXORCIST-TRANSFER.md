# Exorcist transfer comparison — September 11, 2026

**All three conditions passed 9/9. The candidate showed no measured quality gain and used more tokens.** This experiment supports correct behavior on these small tasks, not superiority, production readiness, or general reliability.

| Condition | Strict success | Mean wall seconds | Mean total tokens |
| --- | ---: | ---: | ---: |
| No skill | 9/9 | 43.075 | 63,637.3 |
| Original Exorcist (`be9d038`) | 9/9 | 40.905 | 64,072.8 |
| Candidate Exorcist (`e2eb92b`) | 9/9 | 41.046 | 69,670.7 |

Means are raw arithmetic means over nine cells, **not** the mean-of-task-ratios normalization in the earlier chart. Total tokens = CLI input (cached input already included) + output. No dollar billing estimate. Sample SD and ranges across the heterogeneous tasks are retained in [metrics.json](results/exorcist-transfer-2026-09-11/metrics.json); they are not confidence intervals. Shared host, caching, and small sample size prevent a general speed claim.

## Design and evidence

[Plan](PLAN-EXORCIST-TRANSFER.md) and [task criteria](exorcist-transfer-cases.json) were committed at `33b23a3` before execution. Three tasks cover an acknowledgement-failure duplicate, an effective stable-key safeguard, and missing runtime evidence. These are new domains relative to the development search case, but still author-designed synthetic fixtures, not real repositories or blinded third-party tasks. The duplicate task explicitly asks about the lock, making this a prompted transfer check rather than an unprompted explanation test.

27 fresh Astra-medium sessions ran serially: three tasks × three conditions × three repetitions. Condition order rotated by block as planned. All 27 completed, no timeouts, no explicit account-limit stops, no cell reruns. All 27 thread IDs are distinct. Original production files in every final snapshot match their fixture contents. Raw originals remain in ignored local storage.

Skill snapshots came from pinned Git revisions; [snapshot hashes](results/exorcist-transfer-2026-09-11/snapshots.json) and per-cell metadata identify them. Entrypoint hashes were checked during review. Repository HEAD changed during the experiment due to test/documentation/banner commits; the runner, transfer runner and task file did not change from execution start through completion. Each block manifest retains the actual revision, rather than retroactively assigning a single revision.

The [27 reviews](results/exorcist-transfer-2026-09-11/reviews.json) record author, unblinded judgments in narrative notes against the frozen criteria, not automatic text matching. Each cell contains the final answer, commands/output, events, stderr, diff, source snapshot and hashes of source evidence. [Metrics](results/exorcist-transfer-2026-09-11/metrics.json) link every review to its cell directory. Process completion is not used as a substitute for behavioral review.

## Observations

- All conditions demonstrated sequential duplicate sending without simultaneous workers and explained why a lock does not make an external send and acknowledgement atomic.
- All conditions recognized effective provider deduplication and declined an unsupported production fix.
- All conditions separated optional SDK support from actual stable-key usage when runtime artifacts were missing.
- Some sessions ran extra retries or fresh-provider controls. These can explain assumptions, but were not rewarded as higher quality merely for doing more work.
- Candidate block 2 instrumented provider dictionary writes rather than only final entry count. This is a useful observation, not evidence of systematic superiority; no post-hoc rubric bonus was assigned.
- Candidate block 3 discussed recording successful delivery before acknowledgement, with acknowledgement retries still required and explicit crash/new-instance limitations. It did not recommend marking completion before sending. This distinction matters when auditing its proposed corrective direction.

The candidate remains a narrow explanation correction with no demonstrated comparative benefit here. Do not market it as a performance upgrade. This suite has a ceiling effect: baseline already satisfies every criterion. Keep these cases as regression checks; further utility claims require separately planned realistic tasks, not repeated tuning until these scores look favorable.

## Reproduce and inspect

```sh
python3 benchmarks/run_transfer.py --output benchmarks/local-runs/new-transfer
python3 benchmarks/export_transfer.py --run benchmarks/local-runs/new-transfer --output benchmarks/results/new-transfer
```

Before export, independently review each cell and create `reviews.json` with block, condition, case, three pass/fail/unknown criteria, scope, and evidence notes. The export command intentionally requires all 27 distinct reviews and nine finished blocks for this completed-experiment format; retain and report partial runs separately, never discard them.

Original evidence pattern scanning found 82 private-path matches and no credential/auth-header matches. Export replaced local path prefixes; exported evidence passed the same pattern scan. Manual command/answer review supplemented it. Neither pattern scanning nor author review guarantees absence of every possible secret. No authentication files were exported.

The original [72-session report](REPORT-2026-09-11.md) remains unchanged and contributes no observations to this comparison.
