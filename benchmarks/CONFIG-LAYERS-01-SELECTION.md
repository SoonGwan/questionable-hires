# Configuration-layer audit selection — 2026-09-21

Preparation only. Freeze skills at `e1e1ef8` before native/model outcomes.
This is an authored development fixture, not upstream source, a user incident,
independent validation or a held-out benchmark. It tests existing automation's
operating range, not isolated attribution to the new returning-probe cache.

## Fixed workload

A small Python configuration resolver merges defaults, environment settings and
explicit overrides. Later layers win; `None` means absent while false/zero/empty
values remain explicit. Input mappings must remain unchanged. Existing native
unittest checks cover defaults, one environment value, one override value and
an absent override. They need not cover every interaction.

Audit these four independent replacements in this fixed order:

1. Reverse environment/override iteration order.
2. Replace the `is not None` condition with a truth-value check.
3. Reuse the defaults mapping rather than copying it.
4. Remove the absent-value filter, accepting every value.

Single control requests only the first; repeated-work requests all four. Both
receive identical source/tests and the same explicit contracts. Survivors stay
in the set. Existing tests run unchanged on correct and independently faulty
code. Add and validate a native assertion only where original tests survive.
The task does not prescribe a helper, probe grouping, or cache pattern.

## Gates before model execution

Fresh-import the public module; verify same-process test bindings; execute
original correct/faulty tests and stronger passing/failing assertion controls.
Retain counts, original bytes/modes and cleanup evidence. No artificial waits,
duplicated expensive setup, forced guide reads or tests added solely to favor
automation. Author-native controls are not model work.

Freeze runnable inputs, criteria, exact resources/runtime and a four-cell serial
baseline/current schedule only after preparation. Alternate pair order, Astra
medium, one attempt each. Keep timeouts, adverse results and recoveries; do not
rerun to obtain a favorable result. The two tasks are correlated and cannot
override the adverse all-eight result or establish a broad20–30% improvement.

한국어: 설정 병합의 우선순위·명시적 거짓 값·입력 보존·누락 값 처리4종을
실행 전에 고정했다. 단일/4개 요청의 작성자 제작 개발용 대조이며, 스킬 사용을
강제하거나 새 캐시의 효과를 단독 입증하는 실험이 아니다. 준비 검증 후에만
모델 실행 조건을 확정하고 불리한 결과·살아남는 결함도 모두 보존한다.
