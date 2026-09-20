# Current all-eight screen: correct outcomes, higher token cost

2026-09-20. Launch `8b0c0a7`; resources `62e5886`.
[Frozen protocol](../../ALL-EIGHT-CURRENT-02-PROTOCOL.md),
[inputs/order/hashes](run.json), [preflight](preflight.json),
[all reviewed rows](comparison.json), [separate author controls](author-controls.json).

Sixteen fresh GPT-6 Astra medium sessions completed: eight exposed authored
development tasks × no-skill/current, once each. Each condition went first four
times; execution was serial, not randomized. No timeout, account-limit stop,
excluded cell or replacement model run. This is **not a held-out real-project
study**, and not evidence of broad 20–30% improvement.

Both conditions meet all eight full-task and scope requirements. Current summed
tokens are **22.94% higher**, while summed process time is **5.58% lower**. No
individual pair reduces both metrics. This is not an accepted overall efficiency
win. Keep featured charts and release-performance claims unchanged.

## Every task, including adverse results

Full input + output tokens, cached input counted once; process wall seconds.
Changes compare current with its fresh baseline. Negative means less resource.
Test method counts are not comparable measures of coverage across implementations.

| Role | Baseline tokens / s | Current tokens / s | Tokens / time change | Full task B/C |
| --- | ---: | ---: | ---: | --- |
| Necromancer | 87,246 / 67.635 | 90,284 / 57.990 | +3.48% / −14.26% | pass / pass |
| Receipt | 68,379 / 63.109 | 104,717 / 49.632 | +53.14% / −21.36% | pass / pass |
| Landlord | 62,503 / 32.719 | 65,723 / 31.677 | +5.15% / −3.18% | pass / pass |
| Mother-in-law | 64,722 / 42.604 | 53,034 / 48.811 | −18.06% / +14.57% | pass / pass |
| Exorcist | 63,423 / 51.633 | 68,381 / 49.824 | +7.82% / −3.50% | pass / pass |
| Hostage Negotiator | 88,406 / 116.930 | 175,465 / 123.872 | +98.48% / +5.94% | pass / pass |
| Con Artist | 84,035 / 82.404 | 90,205 / 76.572 | +7.34% / −7.08% | pass / pass |
| Friday | 65,856 / 76.231 | 70,857 / 65.146 | +7.59% / −14.54% | pass / pass |
| **Sum** | **584,570 / 533.265** | **718,666 / 503.524** | **+22.94% / −5.58%** | **8/8 / 8/8** |

Sums are accounting, not task-weighted causal estimates or significance tests.
Shared host/cache, fixed pair order, n=1, previously exposed tasks and different
extra checks limit interpretation. Do not compare older wall times as though
contemporaneous. Mother-in-law, Exorcist and Friday resources were unchanged
since the prior all-eight screen; their fresh variation is not a result of the
five other roles' changes.

## Original evidence review

- **Necromancer:** actual introducing patches and all nine independent invoice
  observations in both arms; three native tests per variant. Both recover from
  unavailable `python` to `python3`; recovery costs stay included. Current uses
  structural AST substitution; baseline exact single-match replacement.
- **Receipt:** same five current tests/schema on both full revisions, two actual
  retry failures and three controls per revision. Both report the incomplete fix.
  Current adopts its helper after reading the interface and 227 implementation
  lines; baseline writes a comparison. Current records import paths/PIDs inside
  each native test process. Baseline separately prechecks copied imports and its
  native tracebacks establish copied tests; do not call that precheck same-process
  instrumentation. Copies/databases removed and original files preserved.
- **Landlord:** both native contract tests and direct Backend behavior verified;
  preserve boolean/exception translation and operational errors. Staging remains
  unknown. No parent-directory instruction search or manufactured staging result.
- **Mother-in-law:** exactly two added methods plus original initial test, one
  native suite run each: two passes and one genuine nested-payload assertion
  failure. Both reuse project support; no production edit or authoring repair.
  Required later checkpoints remain in code and unwind after the failure, as
  explicitly allowed. Current adds pending-state checks and a process deadline.
- **Exorcist:** real fresh-process absent-environment failure `3 != 1`, actual
  setup/import timing, configured native pass and standalone one-call control.
  Baseline adds an uninstrumented run and callback counting; current observes
  actual setup while retaining the original callback-count assertion.
- **Hostage:** same production generation-owned cleanup guard, no serialization.
  Baseline's six methods/subtests cover requested scenarios; its first run has
  five ownership failures plus one cancellation-identity test error, repaired at
  the direct refresh boundary before final six-pass run. Current uses unchanged
  copied support, nine methods, four before failures and nine after passes; no
  test repair, generation-step assertion or unittest method collision. Different
  extras include baseline's callback-cancellation identity and current's None
  result. Current reads full support after its usage block and uses eight recorded
  responses versus baseline's five. Three final shell checks share **one** outer
  parallel call; they are not three model round trips. All costs stay included.
- **Con Artist:** actual same-process bindings and traced writer calls in all
  four phases. Original acknowledgment tests survive commit omission; stronger
  fresh-connection complete binary-row assertion passes correct and rejects
  missing commit. Baseline adds one new method; current strengthens one existing
  method and reruns both. Neither uses the changed helper resources, so this does
  not measure their runtime improvement. Originals preserved, copies removed.
- **Friday:** actual SQL scripts and literal readers at all five checkpoints;
  OLD labels fail at 2–4 despite correct rows, inactive NEW errors at 1/5 are not
  blockers. New binary writes survive down. Both use native SQLite, not the optional
  matrix. Current also checks the base table each step; baseline checks it at end.

All original files outside requested Editor tests and Hostage implementation/tests
remain unchanged, including owner notes. Git HEAD and installed resources remain
unchanged. Commands stay within the requested scope. This inventory is not proof
against every unrecorded effect.

### Capture limitations retained

Six CLI command outputs omit original evidence without a truncation marker.
Their matching stored responses retain it; no model was rerun to repair evidence:

| Cell | CLI item | Original stored line | Missing CLI evidence |
| --- | --- | ---: | --- |
| Baseline Exorcist | item_3 | 28 | Original uninstrumented failing test |
| Current Exorcist | item_4 | 30 | Absent-environment failing test |
| Current Hostage | item_6 | 39 | Prefix of nine-test before run |
| Current Hostage | item_9 | 53 | Entire nine-test passing output |
| Baseline Con Artist | item_5 | 35 | Correct/original phase and fault diff |
| Current Con Artist | item_5 | 36 | Correct/original phase and fault diff |

The mechanical any-output matcher falsely marks Hostage `item_9` exact by matching
another empty successful output. The exported manual exception overrides that
candidate; do not treat mechanical flags as command-correlated proof. Original CLI
and stored records remain intact. No missing, unmatched or duplicate stored tool
call/output IDs were found. Lexical `truncated` flags also match documentation and
`output_truncated:false`; they are not verdicts.

Each current target entry is present in recorded initial context before tools;
baselines show no exact target bodies. Exposure checks do not prove absence of
unrecorded instructions or obedience to configuration requests. Per-response usage
reconciles with final CLI counters in all sixteen cells. Raw private initial
messages stay local; only selected tool records and numeric/context observations
are exported.

## Separate author controls and next decision

Twelve untimed author checks execute delivered suites in owned copies after all
original sessions finish. Both three-test Editor suites reject the shallow
snapshot and pass a conforming deep snapshot. Hostage suites pass their delivered
fix and a valid internal-counter-step alternative, reject the original owner bug,
and both implementations pass an independent six-test oracle. No timeout or
setup error. Original artifacts remain unchanged. These are not additional model
tasks, original before evidence, or a repaired transcript.

The recent Hostage assertion correction is followed in this attempt, but its
token overhead is substantially worse. Do not trade away that reliability or
promote the bundle as faster overall. Next changes should target **observed
orchestration work**, particularly Receipt/Hostage support reading and preparation,
without suppressing justified trust checks or required coverage. Freeze a changed
candidate and a bounded transfer test before new model calls; do not repeat this
unchanged exposed set until it produces a favorable total. Installation/public
release gates and broader real-task confirmation remain separate and incomplete.

한국어: 8개 과제를 무스킬/현재 버전 각 1회, 총 16세션으로 비교했다. 양쪽 모두
작업·범위 기준 8/8을 충족했지만, 현재 버전은 합산 토큰이 **22.94% 늘고** 시간은
**5.58% 줄었다**. 두 지표를 동시에 줄인 과제는 없고, 전체 성능 향상 목표는 아직
미달이다. 특히 Receipt와 Hostage의 추가 비용을 그대로 보존한다. Hostage는 이번에
내부 카운터 고정·테스트 메서드 충돌 없이 작성됐으며 정상 대안도 별도 검증에서
통과했지만, 이것을 토큰 절감 성과로 바꾸어 말하지 않는다. 누락된 CLI 출력 6건은
해당 원본 저장 기록으로 확인했고, 빈 출력을 잘못 일치 처리한 대조 도구의 한계도
공개했다. 정상/결함 대조 검증 12건은 모델 실행과 분리된 작성자 검사다. 반복 없는
기존 개발 과제 결과이므로 대표 그래프를 바꾸거나 보편적 우위를 주장하지 않는다.
