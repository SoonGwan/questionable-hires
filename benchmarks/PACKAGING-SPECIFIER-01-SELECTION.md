# Packaging specifier audit: selection before native outcomes

2026-09-21. Preparation only; no model schedule or performance claim.
Freeze current skill resources at `c8fd471` before inspecting task outcomes.
No candidate instruction change is proposed by this experiment.

Use upstream pypa/packaging tag 24.2, peeled commit
`d8e3b31b734926ebbcaff654279f6855a73e052f`. This older fixed release is selected
for reproducibility, not described as the latest release. Preserve upstream
source, tests and licenses byte-for-byte. The selected native test file is
`tests/test_specifiers.py`, with its original `test_version.py` data dependency.
Source and tests were inspected during selection; this is an author-selected
real-source transfer task, not a blind/independent benchmark or user incident.
Earlier packaging name-policy work used another module/version and no upstream
tests; it is not this task's validation.

## Fixed workload rule

Take the first three `_compare_` methods in source order inside `Specifier`:
`_compare_compatible`, `_compare_equal`, `_compare_not_equal`. For each method,
replace its last return statement in source order with `return False`, keeping
all other code unchanged. Each mutation is independent, never cumulative.
This mechanical selection is recorded before executing correct/faulty tests;
do not replace a surviving mutation with an easier-to-detect one.

Two correlated requests use identical project inputs:

1. Single control: audit only the first mutation.
2. Repeated work: audit all three independent mutations.

Use the original full specifier test file with native pytest, `-x -q --tb=short`
and the cache provider disabled. The same selector/options apply to every
correct/faulty run. Fail-fast is intentional: a genuine first assertion failure
can establish detection, not exhaustive mutant coverage. Baseline must complete
the original file successfully; missing dependencies or import failures are not
fault detection. If a fault survives, report survival and investigate an actual
native regression assertion; do not rewrite existing tests.

Actual test imports must resolve to the supplied local package and the tested
Specifier binding, not an installed packaging distribution. Preserve project
bytes/modes and remove owned scratch. No dependency installation, network,
external project search or publication is allowed during model execution.
Author preparation may obtain pinned dependencies in a task-local environment.

## Before scheduling models

Export exact source/test/license identities, fresh-import the public package,
run the unchanged correct suite and every declared mutation, and retain all
native results. Confirm expected assertion failures rather than support errors;
survivors remain in scope. Verify original bytes/modes and scratch cleanup.
Do not add a sleep, artificial expensive setup, duplicated fault or repeated
suite solely to manufacture an automation advantage.

Prepare baseline/current pairs only after the fixture is operational and freeze
all inputs, criteria, runtime, actual selected resource digests and a one-attempt
schedule. Four sessions, two tasks, Astra medium, alternating pair order are
the intended bounded scope; final execution controls must be committed before
launch. Do not force helper adoption: observe whether existing automation is
chosen and preserves native evidence. Same-process/fresh-copy requirements apply
equally to both arms, not solely to the helper arm.

Retain every scheduled attempt, both cost metrics and recovery. Separate
author preflight from model work. A favorable repeated-work pair cannot override
the adverse eight-role regression or establish a broad20–30% gain. A negative
result is a decision, not a reason to replace tasks or rerun until favorable.

한국어: 고정된 packaging24.2 원본 코드·테스트에서 소스 순서상 첫3개 비교
메서드의 마지막 반환문을 각각 바꾸는 규칙을 실행 전에 정했다. 단일/3개 감사
요청을 함께 준비하며 살아남는 결함도 교체하지 않는다. 기존 스킬을 고정하고
실제 반복 작업에서 사용되는지 보려는 작성자 선정 전이 과제다. 아직 실행 성과나
독립 벤치마크가 아니며, 과거의 불리한 전체 비교를 대체하지 않는다.
