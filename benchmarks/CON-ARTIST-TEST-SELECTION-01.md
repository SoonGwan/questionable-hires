# Con Artist: share recipe setup for required test-specific exits

Candidate parent `f7d91dc`, 2026-09-15. This is an implemented helper capability
with native validation, **not a model-performance result**.

## Observed friction

[Installer transfer 01](results/installer-audit-01/README.md) retains two skill
sessions that repeat large recipes over five CLI calls. The task explicitly asks
for test-specific exits, so removing those executions would change the task.
The helper previously accepted only one shared `tests` selection in a batch.
Its baseline identity already included exact test arguments, but its public
batch schema could not express different required selections.

## Change

Allow optional `tests` arguments per `mutations` entry, using the existing native
runner, isolated copies, integrity checks, deadlines and failure handling. Common
file/import/precheck configuration is submitted once. The same fault can be paired
with each already-required selection; this is not permission to add redundant
suite/individual runs or extra faults. Native facilities remain preferred for small
self-contained audits. No new mandatory SKILL.md procedure was added.

Different arguments invalidate reuse; each selected correct/faulty check runs
separately. Identical consecutive selections can reuse only the existing successful
baseline under the full identity check. Output references still point directly to
the actual earlier check, not to a reused reference. Invalid later selections stop
the batch and preserve earlier returned observations; remaining work is unrun.

## Validation and remaining test

Before the change, the new realistic selection test was rejected as an unsupported
batch field. Afterwards the native checks establish:

- An acknowledgement-only test passes both correct and faulty persistence code.
- A persistence assertion passes correct code and fails faulty code with actual
  `[]` versus expected `['item']`, not a setup exception.
- Switching selections runs a new correct baseline. Repeating the second selection
  references that second baseline. Three audit entries execute five real checks.
- Original files remain byte-identical and owned scratch is removed.
- An empty later selection retains the first audit, reports incomplete and does
  not execute remaining entries.

The complete `test_mutation_helper.py` suite passes **78 tests / 13.775 seconds**;
skill metadata validation and `git diff --check` pass. These are author-native
checks, not Astra measurements. No 20–30% efficiency claim follows. Compare a fresh
helper-relevant task with equal required work and persisted tool responses in both
arms before deciding whether the change reduces whole-task cost. Do not reuse the
old installer's favorable/adverse costs as measurements of this new candidate.

한국어: 테스트별 종료 결과가 필요한 경우 공통 설정을 반복 입력하지 않고 한 번에
제출할 수 있게 했다. 실제 테스트 실행을 생략하는 기능은 아니다. 선택이 바뀌면
정상 코드를 다시 실행하며, 실제 결함 탐지·정상 통과·원본 보존·중간 오류 처리를
검증했다. 관련 78개 테스트가 통과했지만 모델 토큰·시간 절감은 아직 미측정이다.
