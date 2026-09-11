# Hiring plan

## Implemented and checked

- [x] Eight focused skills with Codex UI metadata.
- [x] Local installer with overwrite refusal and failure rollback.
- [x] Portable local marketplace bundle and validated plugin manifest.
- [x] Actual CLI install, enabled listing, all-eight cache comparison, and removal.
- [x] English and Korean README, original banner, and eight worked examples.
- [x] MIT license, contribution guidance, security reporting, and issue/PR templates.
- [x] Deterministic synthetic fixtures with real history where relevant.
- [x] Twenty-four independent three-arm Astra comparison sessions.
- [x] Eight additional clean, missing-evidence, or necessary-change skill sessions.
- [x] Eight automatic-selection sessions with the whole team installed.
- [x] Published answers, command evidence, diffs, metadata, and final snapshots.
- [x] 183 local infrastructure, helper, packaging and fixture tests (current local run).
- [x] Failed package build cleanup, retry and existing-destination preservation.

See the [evaluation report](../benchmarks/REPORT.md) and [installation record](INSTALLATION-TEST.md) for exactly what those checks establish. An earlier eligibility pilot and an excluded single-hire routing pilot are also retained. Passing these smoke checks does not make every future engineering decision correct.

The [current candidate status](../benchmarks/CURRENT-CANDIDATE-STATUS.md) tracks
subsequent skill revisions, realistic transfers and adverse results. The original
report is historical evidence, not the current candidate's performance score.

## Before a stable public release

- [ ] Repeat independent comparisons and add larger realistic project tasks before making performance claims.
- [ ] Exercise broader unrelated prompts to measure automatic-selection false positives.
- [ ] Validate browser-facing skills against actual rendered interaction flows.
- [ ] Verify remote Git marketplace distribution if it is offered as an installation path.
- [ ] Obtain a passing hosted CI run.
- [ ] Owner decides when to switch the repository from private to public and publish a release.

Hosted GitHub Actions currently cannot start because GitHub reports failed account payments or an insufficient spending limit. The repository remains private. Neither billing changes nor public visibility changes have been performed.

## Hiring policy

Keep each hire's job distinct. Add requirements only when realistic evidence shows a gap. Include clean and uncertain cases alongside bug cases. When the baseline does just as well, show that result; when a hire regresses, fix it and retain the earlier evidence.

Next experiments should test difficult decisions in realistic code, not just increase the number of easy examples. Release quality comes from reproducible behavior and clear limits, not an artificially perfect score.
