# All-eight lean screen: mixed results, no production promotion

2026-09-15. Launch `0eb77a3`; current resources `3aaef96`; isolated lean entries
from the frozen [builder](../../lean_entries.py). [Protocol](../../LEAN-SCREEN-01-PROTOCOL.md),
[actual inputs/order/hashes](run.json), [native author preflight](preflight.json),
[all reviewed rows](comparison.json).

Twenty-four fresh GPT-6 Astra medium sessions completed: eight reused authored
development tasks × baseline/current/lean, once each. No timeouts, account-limit
stops, excluded cells or replacement model sessions. Positions were approximately
balanced, not randomized; host/cache were shared. These are **not held-out
real-project measurements** or evidence of a broad 20–30% improvement.

## What happened

All conditions addressed the eight core functional questions. Full-task success,
including the explicit project-only scope, is **7/8 baseline, 8/8 current, 7/8 lean**.
Baseline Con Artist and lean Hostage each ran `find .. -name AGENTS.md -print`.
That parent traversal violates the same project-only boundary in both cases,
even though it printed nothing. Functional correctness does not erase it.

Numbers are full input + output tokens, with cached input counted once; time is
the original process wall time in seconds. B/C/L means baseline/current/lean.
Negative changes use fewer tokens/less time. No dollar estimate.

| Role / task | Baseline tokens / s | Current tokens / s | Lean tokens / s | Lean vs current: tokens / time | Full task B/C/L |
| --- | ---: | ---: | ---: | ---: | --- |
| Necromancer / history-invoice-boundary | 89,046 / 46.830 | 95,556 / 55.316 | 94,630 / 59.893 | −0.97% / +8.27% | pass/pass/pass |
| Receipt / ledger-delivery-b | 71,815 / 58.511 | 111,447 / 47.344 | 80,110 / 34.884 | −28.12% / −26.32% | pass/pass/pass |
| Landlord / store-check-scope | 67,216 / 35.130 | 70,512 / 36.179 | 69,811 / 33.574 | −0.99% / −7.20% | pass/pass/pass |
| Mother-in-law / editor-snapshot-present | 68,936 / 42.725 | 56,016 / 44.898 | 54,814 / 42.080 | −2.15% / −6.28% | pass/pass/pass |
| Exorcist / runner-environment-timing | 66,686 / 39.589 | 72,841 / 49.493 | 87,887 / 50.386 | +20.66% / +1.80% | pass/pass/pass |
| Hostage / refresh-owner-a | 90,424 / 99.567 | 125,554 / 108.396 | 97,427 / 110.105 | −22.40% / +1.58% | pass/pass/**scope fail** |
| Con Artist / sqlite-commit-audit | 71,266 / 67.595 | 96,045 / 76.249 | 92,183 / 70.118 | −4.02% / −8.04% | **scope fail**/pass/pass |
| Friday / view-contract | 69,627 / 65.792 | 103,201 / 62.922 | 90,371 / 66.645 | −12.43% / +5.92% | pass/pass/pass |

Retaining every scheduled cell, total tokens are 595,016 / 731,172 / 667,233;
summed process seconds are 455.739 / 480.797 / 467.685 (B/C/L). Lean's raw totals
are −8.74% tokens / −2.73% time versus current, but **+12.14% / +2.62% versus
baseline**. These are ratio-of-sums accounting, not an accepted aggregate win:
scope success regresses versus current and task-specific extra work differs.
Do not replace the featured benchmark with these totals.

Receipt is a useful candidate, not a confirmed general effect: −28.12% tokens and
−26.32% time versus current on this one attempt, yet +11.55% tokens / −40.38% time
versus baseline. Mother-in-law lean is −20.49% tokens / −1.51% time versus baseline,
but only −2.15% / −6.28% versus current. Baselines must stay visible.

## Evidence review

Every cell includes its original CLI events, answer, diff, project snapshot,
metadata, selected stored tool records, context checks and a `review.json` with
the decisive command IDs. Original full rollouts/private instructions stay local;
catalog names are represented by counts/hash and target membership, not exported
as a personal inventory. Each of the 16 skill cells contains an exact matching
entry in recorded initial messages before the first tool. None of the eight
baseline recordings matches the current target body at that point. This is not
proof of absent unrecorded instructions or enforcement of disable requests.

Of 111 original shell commands, 107 full normalized output/exit pairs match the
selected stored responses. Four CLI outputs omit leading sections without a
truncation marker; the matching stored responses retain decisive original evidence:

- Baseline Exorcist, `item_3`, stored line 26: absent-environment native failure
  `3 != 1`, exit 1, before the correctly captured setup/standalone control.
- Baseline Con Artist, `item_4`, stored line 30: correct-code original tests 2/2,
  bindings, reached writer and exit 0.
- Current Con Artist, `item_6`, stored line 37: correct-code original tests 2/2,
  same-process binding/profile evidence and exit 0.
- Lean Con Artist, `item_6`, stored line 37: correct-code original tests 2/2,
  binding/call evidence and exit 0.

Both captures are preserved; none was repaired by rerunning a model. No missing,
unmatched or duplicate stored tool call/output IDs were found. The lexical
`truncated`-text field is a review candidate only: helper documentation and
`output_truncated:false` also contain that word.

Native results and scope:

- **Necromancer:** all nine requested real invoice results and actual introducing
  patches observed in each condition. All three initially attempted unavailable
  `python`, then recovered with `python3`. Current used structural AST matching;
  baseline/lean used one-match source replacement. All originals preserved.
- **Receipt:** identical five current tests/schema against both full revisions,
  each with two retry assertion failures and three passing controls. All correctly
  report the partial fix. Both skill cells use the unchanged helper; current reads
  381 helper source lines after the interface, lean searches selected source lines.
  Baseline writes its own comparison. Xcode warnings in skill-cell child output
  do not prevent actual tests. Same required work, different orchestration;
  this single run cannot attribute the difference solely to entry length.
- **Landlord:** each runs both local contract tests and direct-call checks,
  preserves adapter semantics and leaves staging unverified. No invented receipt.
- **Mother-in-law:** exactly two added methods plus the unchanged initial method,
  one original suite run each: two passes, one real nested-payload assertion failure.
  No production/support changes or test-authoring repairs. Required later checkpoints
  unwind after the failure, as permitted. [Author controls](author-editor-controls.json)
  separately run the exact delivered suites against original shallow and conforming
  deep-copy production: all three reject the fault and pass the conforming version.
- **Exorcist:** all observe actual startup/setup timing and callback counts.
  Lean adds an A/B/A effective-constant control and costs more than current.
- **Hostage:** all deliver the same existing-generation cleanup guard and cover
  the requested native scenarios. Baseline runs its eight-method suite twice without
  changed inputs; current runs eight once; lean runs five methods with six failing
  subtest/assertion records before the fix and passes afterward. Current copies the
  unchanged controlled-call asset; baseline/lean write local gates. All twelve
  [author controls](author-hostage-controls.json) succeed as intended: delivered
  suites pass delivered/canonical-correct code and reject original broken cleanup;
  the independent six-method author oracle passes every delivered production fix.
  Lean's parent search still fails the explicit scope requirement.
- **Con Artist:** both existing acknowledgment tests survive commit omission;
  same-process actual binding/call evidence accompanies native checks. Stronger
  fresh-connection full binary rows pass correct and fail faulty code. Current also
  strengthens the empty-payload test; lean reruns originals beside its added assertion.
  Baseline's parent search fails scope. All originals/copies otherwise preserved/removed.
- **Friday:** all execute the actual scripts/literal readers at all five checkpoints,
  distinguishing OLD's wrong labels at phases 2–4 from inactive NEW errors at 1/5.
  Updated/inserted binary rows survive down. Current uses the matrix API, others
  native SQLite. Lean's no-match discovery exits 1, leaving its chained status
  command unrun; required SQL checks still complete.

Project changes are restricted to the requested Editor test additions and Hostage
fix/tests/support. Original notes/requirements, Git HEAD and installed skill resources
remain unchanged in all cells; no unwanted retained scratch is found. This final
inventory does not negate the two out-of-scope read attempts or prove every external
effect impossible. Author replays are separate, untimed validation—not model before
evidence, extra scored tasks, or favorable replacement attempts.

## Decision and next improvement

Do **not** promote the all-eight lean rewrite. Keep shipped entries and historical
featured charts unchanged. Preserve Exorcist's stronger stopping guidance and
Hostage's explicit discovery boundaries; reducing entry bytes is not enough.

Carry Receipt and native-QA candidates forward only as hypotheses for independently
specified new tasks. Investigate repeated helper-source reading and redundant
runner/inventory work without suppressing justified trust or compatibility checks.
Freeze next requirements and acceptance before model calls; preserve baseline,
failures and all costs. Do not rerun this exposed set until a flattering total appears.

한국어: 8개 역할을 무스킬/현재/경량 후보 각 1회, 총 24세션으로 비교했다. 핵심
동작은 모두 확인했으나 작업 범위까지 포함한 성공은 7/8, 8/8, 7/8이다. 무스킬
Con Artist와 후보 Hostage가 부모 경로를 탐색해 같은 기준으로 탈락했다. 후보의
전체 기록 토큰은 현재보다 8.74% 적지만 무스킬보다 12.14% 많고, 전체 성능 우위를
입증하지 못했다. Receipt 한 과제에서는 현재 대비 토큰 28.12%·시간 26.32% 감소,
Editor에서는 무스킬 대비 토큰 20.49% 감소가 관측됐다. 반복 없는 개발 결과이므로
일반 성과로 광고하거나 배포본·대표 그래프를 교체하지 않는다. 실패·로그 누락과
원본 응답 복구 근거를 함께 공개하고, 유망한 역할만 새 과제에서 추가 검증한다.
