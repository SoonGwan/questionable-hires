# All-eight checkpoint 09 — reviewed 2026-09-14

Launch `3a7d972`, resources `9071a1c`;
[protocol](BUNDLE-CONTRACT-09-PROTOCOL.md), [18 original cells](results/bundle-contract-09/),
[full pair costs](BUNDLE-CONTRACT-09-INTAKE.md), [export verification](BUNDLE-CONTRACT-09-EXPORT.md).
Nine unchanged exposed authored tasks, baseline/skill once each, Astra medium,
serial, no retries/timeouts/exclusions. All usage is known. No independent
holdout, production trial or all-eight performance guarantee is established.

## Outcome: promising aggregate cost, mixed evidence and per-task regressions

| All scheduled cells | Baseline | Skill | Change |
| --- | ---: | ---: | ---: |
| Input (cache included once) + output tokens | 760,865 | 657,044 | −13.65% |
| Summed process wall time | 572.922s | 460.983s | −19.54% |

Four pairs use more skill tokens; history and schema use more time too. The
aggregate is a ratio of sums, not a confidence estimate, success-only cost or the
historical chart's mean task ratio. Shared host/cache, n=1 and unequal work prevent
causal/general claims. Do not call this a verified 20–30% gain or token parity in
every workflow. Checkpoint 08's −0.58% tokens / −15.08% time remains historical;
the difference between checkpoints does not isolate any individual skill edit.

## Reviewed developer outcomes

- [Boundary and formatter](BUNDLE-CONTRACT-09-BOUNDARY-FORMATTER-REVIEW.md): both
  boundary fixes and tests are byte-identical, with actual before/after evidence
  and eight matching positive/fault controls. Both formatter recommendations are
  supported, but baseline runs seven extra value checks; skill labels its work
  static. Lower formatter cost is not equal execution work.
- [Form](BUNDLE-CONTRACT-09-FORM-REVIEW.md): both retained implementations work
  and tests catch guard/cleanup faults. Baseline unnecessarily rejects a valid
  duplicate returning False; skill accepts it. Skill has six methods versus seven,
  different callback machinery, higher tokens and missing original test output.
- [Search QA](BUNDLE-CONTRACT-09-SEARCH-REVIEW.md): all four original native
  captures contain decisive evidence. Twelve controls confirm both suites accept
  valid alternatives and distinguish differing intermediate-display contracts.
  Both skill pairs cost less, with different witnesses and artifacts.
- [History and schema](BUNDLE-CONTRACT-09-READONLY-REVIEW.md): both conclusions
  are supported and original Python witnesses replay. Neither skill reads its
  optional helper; the cost regressions cannot be blamed on helper-source reading.
- [Persistence and diagnosis](BUNDLE-CONTRACT-09-AUDIT-REVIEW.md): actual mutation
  binding and stored-list failure are present, with one baseline capture gap.
  Con Artist no longer reads its implementation in this task. Both diagnosis
  probes reproduce response-order races through actual transport; baseline also
  creates a report and saved JSON. Production cache behavior remains unknown.

The final [schema fault controls](results/bundle-contract-09-schema-faults/author-replay.json)
use each original witness unchanged, altering only down SQL in disposable copies.
Both pass the supplied migration and reject deleting the inserted row, deleting
the updated row, or corrupting the untouched row: **8/8 expected results**, all
via before/after row-list AssertionErrors, not setup failures. The
[script](replay_bundle_contract_09_schema_faults.py) verifies witness provenance
against original commands and preserves retained projects. No production migration
was executed, and these controls do not prove application-writer compatibility.

## Original evidence is not repaired by later replay

Two original captures remain incomplete:

1. Form skill: final diff/status present, native test identities/count/output absent.
2. Persistence baseline: first correct-code/existing-test phase absent; later
   phases and stored-list failure present.

Final answers and passing replays cannot fill these gaps. Do not assign strict
18/18 success or promote a favorable replay count into a model win rate. Baseline
persistence replay also refreshes its copy's Git index; that difference remains
reported. Raw usage/resources reconcile, and export redaction preserves evidence
and original hashes. Replays never overwrite original model output or projects.

## Decisions after this checkpoint

Keep the capability corrections, but do not publish a universal speedup claim or
promote these exposed n=1 observations into the featured graph. Preserve adverse
pairs and the baseline test false positive alongside favorable outcomes. Avoid
more rule accumulation based on an unproven explanation for the two cost regressions.

The next implementation investigation is the pending-form overhead and its failure
to qualify a final pass claim when native output is absent. Any new instruction
must preserve callback ownership, valid duplicate behavior and bounded cleanup,
and be tested on new task variants before another full-bundle screen. Runtime
capture defects and skill decision defects must remain distinguishable. Do not
repeat checkpoint 09 until its numbers become favorable. General real-developer
usefulness and broad performance remain the active, unfinished objective.

## 한국어

이번 9개 과제·18세션 검토는 마쳤다. 합계 토큰 13.65%·시간 19.54% 감소지만
4개 과제의 토큰은 늘었고 이력·스키마는 시간도 늘었다. 작업량 차이와 단일
반복, 기존 노출 과제이므로 일반적인 성능 향상이나 20–30% 달성을 주장하지 않는다.

원본 출력 누락은 폼 스킬과 저장 감사 기본 모델의 2건이다. 별도 재실행으로
이를 채우지 않는다. 기본 폼 테스트의 정상 대안 오탐, 스킬의 유리한 결과,
불리한 비용을 모두 보존했다. 마지막 롤백 손실 대조 8회도 실제 값 단언으로
검증했다. 스킬 전체의 실사용·성능 목표가 완료된 것은 아니며 대표 그래프는
유지한다. 다음은 폼 스킬의 비용과 근거 없는 통과 보고 문제를 개선할 차례다.
