# Receipt selection 01: native controls for a new matched workflow pair

2026-09-15, parent `ca3da48`. **No model sessions or performance result.**

[Case builder](receipt_selection_cases.py) supplies an authored stock-allocation
service with actual Git history and five native unittest tests. Repeated SKU
lines must accumulate and insufficient orders must fail without mutating stock.
Before overwrites repeated quantities; after accumulates them. Input types,
invalid quantities/unknown SKUs and empty orders have explicit contracts.

There are two support conditions of **one business scenario**, not two independent
real-world projects. One includes a documented existing native comparison command;
the other has only the application, tests and ordinary test instructions. The
implementations, assertions, task and criteria are identical. Both conditions let
the model choose a valid method; helper usage is not a scored requirement.

## Actual native preflight

[Executable controls](../tests/test_receipt_selection_cases.py) construct both Git
projects inside author-owned project-local temporary roots. The present condition
executes its literal comparison command, then the unchanged Receipt helper. The
absent condition executes the helper with the same current tests and historical
implementations. Each of these three paths runs both variants:

- Before: five native tests, **two failures/three passing controls**. Duplicate
  allocation produces `{'a': 5, 'b': 4}` instead of `{'a': 3, 'b': 4}`; aggregate
  shortage fails to raise `ValueError`. These are intended behavioral assertions,
  not setup exceptions. Test-process exit 1.
- After: the same five tests all pass, exit 0. Distinct lines, empty orders and
  invalid orders remain controls.
- Same-process copied module evidence, source/resource bytes and modes, Git status,
  project-local scratch placement and cleanup are checked. Helper runs also verify
  no timeout/output truncation and whole-tree preservation.

The native project command is intentionally small and specific, not another
general-purpose skill helper. It uses existing Python/native unittest, freezes
current tests and runs only historical `allocation.py` variants. No dependencies,
network, model calls or changes to installed skills.

The initial two author tests passed in 0.830 seconds. They exercise six native
suite executions in total, not two model tasks or a speed comparison. After
clarifying the already-intended input contract, both controls passed again in
0.831 seconds before any model exposure. Repository validation, featured-language
synchronization and whitespace checks also passed. This does not replace a
measured model result.

## Planned comparison and boundaries

Compare baseline, the pre-selection Receipt resource (`6cf9fb1`, identical helper
to current), and the selection revision (`ca3da48`) on fresh instances of both
conditions. Freeze runner, schedule, hashes and criteria before starting models.
Preserve all attempts and inspect actual tool/context records. The four criteria
require identical native work, decisive before/after evidence and exits, actual
revision/import identity, and scope/preservation/cleanup.

Do not penalize a valid native solution in the absent condition or a valid helper
solution in the present condition merely for disagreeing with an expected choice.
Tool choice describes behavior; equal-work total tokens/time and task success
determine whether the revision helps. A faster incomplete result is not a win.

This is a development routing probe with author-supplied facilities. It cannot
establish broad real-developer benefit, independent generalization, or a gain
across all eight roles. It complements rather than replaces actual-source tasks
and the full goal. No existing graph or historical result is changed.

한국어: 주문 재고 배분이라는 새 작성 과제에서 기존 비교 도구가 있는 경우와
없는 경우를 만들었다. 하나의 업무 시나리오를 짝지은 실험이며 실제 프로젝트
두 개의 성과가 아니다. 양쪽 실행 방법에서 결함 2개 실패·정상 대조 3개 통과,
수정 후 5개 통과와 원본 보존을 확인했다. 도구 선택 자체로 정답을 강제하지 않고
동일한 요구사항의 성공 여부와 전체 비용을 비교한다. 모델 실행은 아직 시작하지 않았다.
