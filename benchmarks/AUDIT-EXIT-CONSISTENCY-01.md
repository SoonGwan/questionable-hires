# Native unittest result/exit consistency

2026-09-21, parent `d5eab87`. A demonstrated helper correctness defect, not a
model-efficiency result or a claim about failure frequency in real projects.

## Reproduction before correction

Two new actual-process controls use the existing module-invocation test project:

1. A shutdown handler calls `os._exit(0)`. The correct suite passes; the mutant
   suite records `successful:false` and `AssertionError: 0 != 1`, but native exit
   is0. The helper previously returned `observed` with mutant check exit0.
2. Both suites have a weak assertion that passes; only the mutant registers a
   shutdown handler calling `os._exit(1)`. Native exit1 disagrees with recorded
   `successful:true`. The helper again returned `observed` instead of incomplete.

The first does not establish survival and the second does not establish detection.
The guide already required reading assertions, so `observed` was never itself a
killed-fault verdict; nonetheless the helper should stop on internally conflicting
evidence instead of allowing downstream decisions/baseline reuse from its exit.
These are authored adversarial controls, not observed user incidents.

Before the fix: Python3.9.6 module suite16 tests,2 assertion failures,2.991s.
Both failures were the expected `observed != incomplete` assertions.

## Correction and verification

When completed module-suite success disagrees with native exit success, check
exit becomes7 and an `incomplete_reason` explains the contradiction. The original
native exit, suite observation and captured transcript remain unchanged. Existing
incomplete-check handling stops subsequent work. Timeouts, missing evidence,
all-skipped suites and ordinary pass/failure semantics remain distinct.
No retries, extra child processes or additional entrypoint instructions are added.
This is not a sandbox against tests intentionally forging observation records.

- Python3.9.6 module suite:16 passed,2.935s. Existing real normal/fault assertion
  controls continue to pass; both new contradiction controls stop as incomplete
  and verify source preservation/owned scratch cleanup.
- Python3.11.16 complete audit suite:111 passed,16.572s.
- Repository/skill validation, whitespace and featured-sync checks pass.
- The previous1,101-test full-suite checkpoint remains tied to`c329fb7`; this
  focused run is not relabeled as a new complete-project/platform matrix.

Historical model artifacts and charts are not rescored or regenerated. No model
session was launched and no token/time savings are inferred. This change supports
trustworthy verification; broad skill performance remains unfinished.

한국어: 실제 테스트 기록과 종료 코드가 모순돼도 정상 관찰로 처리하던 결함을
두 프로세스 대조로 재현해 수정했다. 모순은 검증 불완전으로 중단하며 원본 기록은
보존한다. 감사 테스트111개가 통과했다. 작성한 경계 대조의 신뢰성 개선이며,
사용자 환경에서의 발생 빈도나 모델 성능 향상 수치로 주장하지 않는다.
