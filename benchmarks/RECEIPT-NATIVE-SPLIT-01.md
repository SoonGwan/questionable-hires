# Receipt native split01 — compatibility gate, 2026-09-28

Parent`1b85702c`; isolated code-layout candidate only. Ordinary installed/deployed
Receipt remains unchanged. The [guard output01 model records](RECEIPT-GUARD-OUTPUT-01-REVIEW.md)
show large helper reads and combined source-output truncation in three of four
sessions. Existing instruction/read-budget experiments did not establish a general
fix. This candidate tests a runtime partition before any model schedule.

[Transformation](receipt_native_split_candidate.py) moves unchanged Python/Node
startup strings, native check interpretation and process capture into native.py.
compare.py retains recipe validation, snapshotting, revision selection, copying,
original/tree guards and CLI. Existing call names stay available; actual capture,
read and assertion-startup instrumentation is passed at the observed boundaries.
The local source loader uses runpy rather than changing sys.path or writing a native
module bytecode cache. Bytecode behavior still requires actual verification before
adoption. Loading trusted package code is not a sandbox.

Source size: compare.py43,772→27,952 bytes, with17,162 bytes in the new companion.
The total grows to45,114 bytes. These are bytes, not model tokens or saved work.
An agent that needs both sources may read more or require another response.

## Fixed native gate

[Controller](results/receipt-native-split-01/control.py) runs the same ten current
native test modules in ordinary and candidate Git-free copies, serially. Existing
fixtures provide real positive and defective assertions, bootstrap/module/Pytest/
Node entrypoints, assertion observation, timeout/cleanup, guards and multiple
versions. Node24 and the existing Python environment are used; no installation,
model call, approval change or user-project mutation. Preserve every result.

Do not alter the two existing tests that relocate only compare.py. They exercise
a known one-file CLI caller, and the new required companion is a compatibility
concern. Passing full-package calls cannot silently replace that requirement.
Require identical child program strings and unchanged functional assertions.
Any failed existing caller blocks adoption and paid model timing at this checkpoint;
record the exact failure, not just a smaller source file or otherwise-green suite.
No featured/chart/README capability/installed resource change follows preparation.

한국어: 긴 하위 실행 코드를 분리하는 격리 후보다. 진입 파일은 작아지지만 전체
리소스는 커지고 추가 파일을 읽을 수 있으므로 토큰 절감으로 계산하지 않는다.
기존 파일 하나만 복사하는 CLI 검사도 그대로 유지한다. 이 호출 방식이 깨지면
정상 설치 경로가 통과해도 채택하거나 모델 성능 실험을 진행하지 않는다.

## Original native execution — decline

Frozen execution **`f80c1448`**. [Both original arms](results/receipt-native-split-01/results.json)
and [identity](results/receipt-native-split-01/identity.json) retain source and
transform hashes. The controller terminates exit1 as required by its failed gate;
no model call, retry or substituted case occurs.

- [Previous](results/receipt-native-split-01/previous.txt):126 native test methods
  pass, no skips, exit0.
- [Candidate](results/receipt-native-split-01/candidate.txt):the same126 methods,
  124 pass and2 fail, no skips, exit1.
- All five emitted native program strings match exactly. This is identity of the
  child source strings, not proof of general behavioral equivalence.

Both failures are the unchanged one-file relocation consumers:
`test_cli_reports_guard_and_native_results` and
`test_cli_accepts_invocation_and_rejects_invalid_modes`. Each copied compare.py
exits1 with FileNotFoundError loading the absent native.py, before it can return
its required native observations. These are candidate regressions, not missing
pytest/Node setup or a reason to edit the existing assertions. Full-package
positive controls do not repair that standalone caller.

The entry script is36.14% smaller, but the combined scripts are3.07% larger.
Neither measure is a token saving. Do not compare the recorded suite durations:
the failed relocation paths stop early and the work is unequal. Runtime module
cache/thread considerations are not fully validated; this failed compatibility
gate already prevents promotion. No paid model timing is justified.

**Do not adopt this split or replace the two callers to manufacture a pass.**
Keep the ordinary self-contained comparison entry and its deployed behavior.
This closes this partition candidate without changing the previous
[scoped interface cost result](RECEIPT-GUARD-OUTPUT-01-REVIEW.md), historical all-eight
result, featured pointer, personal installation or public download. Full eight-role
quality and joint whole-task token/time improvement remain unmet. Any future
partition must first preserve the existing relocation contract, not silently
exclude it or repeat this unchanged candidate for a favorable outcome.

한국어: 기존 버전126개 통과, 분리 후보는 같은126개 중124개 통과·2개 실패다.
실패는 파일 하나만 복사하는 기존 CLI 경로이며 새 native.py가 없어 네이티브
검사 전에 종료됐다. 진입 파일36.14% 감소는 토큰 절감이 아니고 전체 코드는
3.07% 늘었다. 기존 검사를 바꿔 통과시키지 않고 후보를 폐기하며 모델 실험0회,
설치·공개 배포 변경0회로 마친다. 이전 제한된 절감 결과와 전체8개 미달은 유지한다.
