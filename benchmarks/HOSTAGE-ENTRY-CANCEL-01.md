# Plain callback-entry cancellation correction — 2026-09-21

Parent `b9a2900`. Actual Python asset correction, not an instruction-efficiency
experiment or a new model result. Earlier failed Hostage conditional/completion
guides remain rejected; no generic lifecycle rule or new helper API is added.

## Reproduced behavior

`ControlledCall.started()` previously awaited
`asyncio.wait_for(self._entered.get(), timeout)`. In the locally tested
Python3.9/3.11 runtimes, queue-get completion overlapping waiter cancellation
could return the entry instead of propagating cancellation. The caller's expected
cancelled-wait path therefore did not execute. This is a concrete asset behavior,
not a claim that the historical model runs encountered this race.

The new native regression starts the waiter, lets its queue wait initialize,
starts the application callback, and schedules waiter cancellation in that
wakeup window. Before the fix it fails with **CancelledError not raised** on
both Python versions; the companion competing-consumer control passes.
No import/setup exception accounts for the failure.

## Correction

Plain `started()` now waits for entry-availability notification, not a cancellable
child that consumes the queue item. It dequeues only when returning the entry.
One monotonic deadline is retained through competing-consumer wakeups; the owned
notification task is cancelled/drained in finally. This matches the notification
approach already used by `started_before`, without changing that method, task
ownership, callback result/error identity or the JavaScript asset.

The regression verifies waiter cancellation, the still-pending application,
retrieval of the exact preserved call through `started_before`, and delivery of
the exact chosen result. A second control gives two competing plain waiters
separate successive entries without duplication. Existing timeout, application
cancellation, task-aware waiting, reverse completion and real application controls
remain included. Timing sleeps yield event-loop turns; no wall-clock performance
threshold is used as the behavior oracle.

The usage block and both README capability rows describe the cancellation
behavior. This is cooperative same-loop support, not cancellation of application
work or a blocking-code/process timeout. Already returned entries are delivered;
cancellation does not undo a completed observation.

## Validation

- Before fix:2 focused methods on each Python version; cancellation race fails,
  competing-consumer control passes. Original probe also returned the call despite
  waiter cancellation. These failures are retained in this report, not a green-only
  account of the change.
- After fix: `test_controlled_call_asset.py`,18 methods pass on Python3.9 in0.273s
  and Python3.11 in0.135s. Includes standalone-copy and real application controls.
- `test_owned_tasks_asset.py`:11 pass on Python3.9 in0.812s.
- Complete-usage excerpt check:1 passes on Python3.9 in0.008s.
- Build13 and standalone archive4 pass. Skill quick validation, repository
  metadata/links, featured bilingual synchronization and whitespace checks pass.

The previous1,052-test whole-checkout result predates this fix; it is not relabeled
as a full-suite run of this candidate. No hosted result, model token/time saving,
general correctness guarantee or all-eight improvement is claimed. No new model
sessions were launched, and no featured numeric/chart data changed.

한국어: 호출 진입과 대기 취소가 겹칠 때 취소를 무시하고 호출 객체를 반환하는
문제를 Python3.9·3.11에서 재현했다. 대기는 알림만 기다리고 실제 반환 시에만
호출을 꺼내도록 수정했다. 취소 전파·호출 보존·앱 작업 분리·기존 동작을 검증했다.
이는 도우미 결함 수정이며 모델 성능 향상이나 토큰 절감의 증거는 아니다.
