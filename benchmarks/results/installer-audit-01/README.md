# Installer audit transfer 01 — reviewed 2026-09-15 KST

**No efficiency win.** All four fresh sessions detect their selected real fault,
but skill tokens are materially higher. Launch `8955cb1`, Con Artist resources
`07166bf`, Astra medium, serial, one repeat per arm/case, 240-second deadlines.
See the [frozen protocol](../../INSTALLER-AUDIT-01-PROTOCOL.md),
[input cases](../../installer-audit-01-cases.json), [run manifest](run.json) and
[metadata summary](summary.json). No retries, exclusions or timeouts.

| Task | Baseline total tokens | Skill total tokens | Change | Baseline seconds | Skill seconds | Change |
|---|---:|---:|---:|---:|---:|---:|
| Copy-error rollback | 105,024 | 207,194 | +97.28% | 89.909 | 86.770 | −3.49% |
| Cancellation | 87,695 | 153,745 | +75.32% | 76.401 | 81.199 | +6.28% |

Tokens are input (cache included once) + output; time is full process wall time.
Two authored tasks share one pinned real installer and four unchanged test bodies;
this is neither an independent holdout nor evidence across eight skills. Shared
host/cache, n=1, different orchestration and work volume prevent causal attribution.
No featured chart changes or broad 20–30% claim.

## Original behavioral evidence

- Rollback [baseline commands](installer-audit-rollback--baseline--1/commands.json),
  item_5: moves rollback registration after copying. Eight one-method processes:
  correct four passes; faulty one pass/three assertion failures. Each process runs
  one native test with exit 0/1. Copied module/code paths, executed installer lines
  and remaining destination entries are observed in the actual test processes.
- Rollback [skill commands](installer-audit-rollback--skill--1/commands.json),
  item_8: same fault, correct four-pass suite, faulty one-pass/three-fail suite.
  Items 9–12 additionally run all four methods separately against both versions.
  Native check exits, assertions and same-process bindings/trace are present.
- Cancellation [baseline commands](installer-audit-cancellation--baseline--1/commands.json),
  item_4: outer `BaseException` handler narrowed to `Exception`. Correct four-pass
  suite, mutant three-pass/one-fail suite, plus eight one-method processes.
  Traces show copied execution, both leftover targets, preserved `user.txt` bytes
  and original cancellation identity.
- Cancellation [skill commands](installer-audit-cancellation--skill--1/commands.json),
  item_7: same fault and native suite results. Items 8–11 supply the eight individual
  method executions with matching outcomes. Copied test binding/function code,
  executed installer, leftover targets and marker bytes are observed.

Rollback failures are actual assertions at test lines 278 (unexpected `receipt`),
303 (unexpected `receipt` after cancellation) and 325 (cleanup attempts omit
`receipt`). Cancellation fails line 303 with both installed skill directories
remaining, while the preceding identity assertion passes. No setup errors or
stronger probes; existing tests already detect each chosen fault. Physical disk
exhaustion is not tested: existing mocks inject copy/cleanup errors. Other possible
interruption timings and interactions remain untested.

The task explicitly requested test-specific exits. All agents interpreted that
as individual process exits, so those checks cannot simply be called gratuitous.
However, rollback baseline only runs individual methods, whereas the other three
sessions also run grouped suites. Thus work volume is unequal even though native
coverage and detecting assertions agree; do not call the small time difference an
accepted win. No clean-input false-positive rate or full-suite success is measured.

## Cost diagnosis and integrity

Baseline uses 4/3 commands (rollback/cancellation); skill uses 12/11. Both skill
sessions read the common guide and helper source excerpts, implement execution
tracing, then repeat large recipes across five CLI calls. Cancellation baseline
groups the same ten native processes in one author-created command. These are
observed differences, not isolated causes of token/time differences.

All 12 supplied final project files match frozen input bytes in all cells, with
no retained scratch. Original logs include preservation checks; helper checks
cover its 10 selected files' bytes/modes and owned scratch. Installed skill resource
manifests are unchanged. These checks are not whole-filesystem race protection.

All original completed-command objects, outputs and final usage were reconciled
against this export after path redaction. Each `source-sha256.json` matches its
retained local originals. Full fixture files, original command streams and model
answers are included; no author replay or repaired run supplies missing evidence.
Native unittest abbreviates some path representations and long diffs; the original
traces provide the concrete destination entries. Helper outputs have no reported
truncation or timeout. A successful collector exit alone was not used for scoring.

Decision: retain this adverse transfer result. Improve concrete documentation/API
friction, then evaluate a changed candidate; do not repeat the unchanged candidate
until a favorable draw appears. Keep broader performance explicitly unproven.

한국어: 실제 결함 탐지는 네 실행 모두 확인됐지만 스킬 토큰은 기본 모델보다
97.28%·75.32% 많았다. 시간은 −3.49%·+6.28%로 일관된 개선이 아니다.
도우미 사용법 확인과 반복 호출이 관측됐으며, 테스트별 종료 코드 요구도 추가
실행에 영향을 줬다. 두 과제는 같은 설치 구현을 공유하고 반복은 1회뿐이다.
불리한 결과와 원본 실행 기록을 보존하며 성능 목표 달성이나 대표 그래프 변경의
근거로 쓰지 않는다. 수정할 것은 구체적인 사용 마찰이지 수치나 기존 판정 기준이 아니다.
