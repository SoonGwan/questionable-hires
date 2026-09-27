# Effort01 Editor outcome follow-up — 2026-09-27

Execution protocol `72f67ad6`, measured skill candidate `7172b50c`.
This is a scoped follow-up to the [terminal16 checkpoint](ALL-EIGHT-EFFORT-01-TERMINAL16.md).
It closes the pending Editor conforming-production check, not the complete
all-eight quality review or the owner objective. Costs and original attempts
are unchanged; current Receipt guidance `f91d8ef0` was not measured here.

## Original model evidence

Both conditions retain the initial test and add exactly two native async methods.
Both first attempt unavailable `python` (exit127; no tests), then run python3.
The actual suite runs three methods: two pass and the pending full nested payload
assertion fails when live theme changes from dark to blue. Medium CLI output is
empty for that command; its exact corresponding stored-session tool response
contains the native failure and three-test count. This is recovered original
output, not a rerun substituted into the model transcript.

Source review: the existing writes helper records a deep copy only after
acknowledgement. Both tests exercise real Editor.save, use independent full
nested expected values, observe callback entry, bound waits, and register owned
cleanup through the helper. The pending-save test asserts its payload before
acknowledgement, then retains stored payload/current settings/dirty assertions.
The early regression assertion unwinds to cleanup, so those later assertions
were not executed on defective production. The source contains them; original
execution must not be described as having reached them. Production and other
initial files remain unchanged; installed skill resources match their originals.

## Separate author evidence after timing

The existing `review_editor_snapshot.py` is reused on separate temporary copies;
no model calls, original workspace changes or new timing measurements.
[Native results and source checks](results/all-eight-effort-01-editor-review/author-replays.json)
retain four runs. Medium and low each fail the original shallow-copy code with
one assertion failure and two passes (native exit1). Replacing only the known
shallow snapshot with deepcopy in the disposable author copy makes all three
native tests pass (exit0) for each condition. This demonstrates that the retained
post-acknowledgement checkpoints execute on conforming production rather than
being dead test code. This source-level counterfactual is not an application fix,
an independent case, or original model success evidence.

Both conditions support the supplied Editor regression task. Low performed one
additional dirty-state assertion before acknowledgement; medium used an explicit
15-second subprocess bound. Preserve unequal work and the failed interpreter
launches in costs. The measured low cost reduction remains tiny (tokens−0.66%)
and cannot justify all-role default adoption. Full other-role scope/output review,
external validation and actual next-version measurement remain separate gates.

한국어: 두 조건 모두 원래 테스트를 보존하고 실제 저장 진입·지연 직렬화·전체
중첩 값·독립 기대값·제한된 대기·작업 정리를 검사했다. 원본 버그에서는 저장
도중 페이로드가 바뀌는 단언이 실패하여 후속 단언은 정리로 빠졌다. 별도 복사본의
올바른 깊은 복사 구현에서는 세 네이티브 테스트가 모두 통과해 후속 검사가 실제
실행됨을 확인했다. 이 네 번의 작성자 확인은 모델 원본 결과·시간·토큰을 바꾸지
않으며 전체8개 품질 검토나 새 Receipt 안내의 성능 측정을 대신하지 않는다.
