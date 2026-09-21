# Request-entry waiter cancellation correction — 2026-09-21

Parent`eed4ff7`. The native-test `ControlledFetch.started` asset had the same
queue-get cancellation window previously repaired in the separate
[Hostage callback asset](HOSTAGE-ENTRY-CANCEL-01.md). This is a concrete runtime
correction, not an inference that prior model sessions encountered the race.

## Failing-first reproduction

Two new controls in [the native asset tests](../tests/test_controlled_fetch_asset.py)
start the entry waiter, yield loop turns, start an actual application fetch, and
schedule waiter cancellation during wakeup. Before the fix, Python3.9.6 and
Python3.11.16 each run8 methods:7pass,1failure, specifically
`AssertionError: CancelledError not raised`. The competing-consumer control
passes; this is not an import/setup failure or a wall-time benchmark.

## Correction and coverage

Wait for an entry-availability event rather than a child task that consumes the
queue item. Dequeue only when delivering the request. Use one deadline through
competing-consumer wakeups, cancel/drain the owned notification task in `finally`,
and leave application-task ownership with the test. No new helper API or
cross-skill dependency is introduced; the copied transport remains standalone.

The repaired race control confirms cancellation reaches the waiter, the actual
application remains pending, a subsequent waiter retrieves the request and the
exact chosen result reaches that application. The competing-waiter control
delivers distinct request futures once each despite identical keys. Existing
wrong-key actual/expected evidence, timeout bounds, error identity, reverse
completion, sibling cancellation and standalone-copy controls remain passing.

After correction:8/8 controls pass on Python3.11.16 in0.084s and Python3.9.6
in0.207s. The38 `test_mother*.py` methods pass on Python3.11 in1.001s. These are
focused compatibility checks, not a new full release matrix. Loop-turn yields
make the native race reproducible; they are not delays added to a model task.
Build13 and standalone packaging4 tests also pass (3.080s/1.094s). A fresh
`git archive c00276d`, without Git or local-run state, passes all8 native asset
tests on Python3.11.16 in0.086s with no skips. Skill/repository validation and
featured bilingual synchronization pass; no hosted result is inferred.

The native guide and both capability rows now describe the behavior. No generic
skill-entry rule, sequence-probe behavior, production code, frozen model result
or featured chart changed. Already returned handles are consumed; cancellation
does not undo an earlier completed observation. Cooperative same-loop behavior
does not provide blocking-code interruption or process containment.

This improves trustworthiness of test support, not demonstrated model token/time
cost. The full user efficiency objective and hosted-release gate remain unmet.

한국어: 요청 도착과 대기 취소가 겹칠 때 취소가 무시되는 오류를 Python3.9·3.11에서
먼저 재현했다. 알림만 기다리고 전달할 때 요청을 꺼내도록 수정해 취소 전파·요청
보존·앱 작업 분리·중복 키 요청의 독립성을 검증했다. 테스트 도구의 실제 결함
수정이며 모델 성능 개선율이나 전체 배포 검증 완료로 주장하지 않는다.
