# Receipt module completion01 — 2026-09-27

Candidate on parent **`96d43558`**; exact modified source identities are retained
in [source hashes](results/receipt-native-completion-01/source-sha256.json).
This is a local capability correction, not a new model-efficiency measurement.
Integration05 stays tied to `75183f2f`; native-split02 stays tied to `6c099d68`.

## Concrete fault and correction

An actual `python -B -m unittest` test body prints its entry and then calls
`os._exit(0)`. Before this correction, Receipt completes same-process import
verification before entering the suite, sees native exit0, reports `observed`,
and executes the next comparison even though no test result completed.
The new regression fails against the original helper: `observed != incomplete`.
This is different from the existing import-time exception guard.

The startup adapter now observes the actual `unittest.TestProgram.runTests`
result. It records tests, skips and success only when that native program returns
or raises with a completed result. The parent retains `native_exit_code`, import
provenance and native output; missing completion or disagreement maps check7,
CLI2/incomplete, and stops later comparisons. A deliberate failure whose atexit
hook masks native exit to0 also remains incomplete, with its actual AssertionError
and completed unsuccessful result preserved. The early-body control now executes
one check instead of two; this is an authored invalid-evidence control, not
measured whole-task performance.

Completed empty/all-skipped native exits remain observations, not passing
regression evidence. The documented newer-Python empty exit5 is accepted for a
successful completed zero-test suite; a local synthetic exit substitution control
verifies that branch without claiming actual execution on another Python version.
[Official unittest documentation](https://docs.python.org/3.13/library/unittest.html#unittest.main)
identifies exit5 for no executed/skipped tests. Local actual validation uses
Python3.11.6. The existing Con Artist native observer already uses the same
completed-result distinction; no new cross-skill dependency is introduced.

## Execution evidence and limits

- Original failing reproduction: one actual regression, native test-body entry,
  expectation failure `observed != incomplete`; no source change had been made.
- Draft validation:90 relevant comparison/native/guard controls pass; broader
  Receipt discovery196 tests passes. These are before the final empty-exit5
  compatibility branch/control; they are not relabeled as final197-test evidence.
- Final native controls:16 tests pass7.066s; catalog metadata/local links pass.
- Separate disposable Git-free source copies retain an actual old-helper failure
  and final16-test native pass7.167s. These later author observations are separate
  from the first original reproduction; [both outputs](results/receipt-native-completion-01/)
  and [selections](results/receipt-native-completion-01/archive-checks.json) are kept.

Controls preserve before/after native failures, same-process imports, source-layout
lookup, real configured startup hooks, child lookup, source tree and scratch
cleanup. The CLI installed-path copy check remains covered. These checks do not
establish a new full catalog installation, remote release or platform matrix.

This changes only supported module-unittest comparison. Bootstrap, pytest and
Node modes retain their contracts; no generic early-exit detection claim is made.
Observations remain instrumentation of trusted tests, not tamper-proof attestation,
required coverage, dispatch proof or a verified fix. A test can have unspecified
side effects; copies/guards do not create a sandbox. No frozen input, old result,
featured chart or model usage counter is changed.

The next candidate still needs actual model evaluation on distinct relevant
workflows plus ordinary controls, preserving quality and requiring both lower
tokens and faster time before an efficiency claim. Broader all-eight developer
quality/cost goals remain unmet. Do not rerun exposed integration05 until favorable.

한국어: 실제 테스트 본문이 종료 코드0으로 중단되면 기존 helper는 검사가
완료되지 않았는데도 관찰 완료로 처리하고 다음 비교를 실행했다. 이제 완료된
unittest 결과와 native 종료값을 함께 확인하며, 누락·불일치는 check7/CLI2로
중단한다. 최종16개 네이티브 검사와 Git 없는 복사본 검사가 통과했다. 초안의
196개 검사를 최종 버전 전체 검증으로 바꾸어 표기하지 않으며 모델 토큰·시간
절감이나 전체8개 역할 목표 달성은 아직 입증되지 않았다.
