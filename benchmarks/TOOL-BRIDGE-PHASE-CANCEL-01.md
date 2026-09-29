# Direct tool phase cancellation01 — native prototype, 2026-09-28

Source parent `026a8312`. No model calls, ordinary skill edits or registration.
The [model approval failure](RECEIPT-BRIDGE-ROUTE-01-REVIEW.md) remains unresolved;
this local SDK lifecycle control neither changes nor bypasses that model gate.

Before execution: compare unchanged HTTP cancellation behavior against a launch
flag checking cancellation before/after each native `run_check`. Both arms use the
same isolated adapter with identical phase logging. The current subprocess drains
under existing native cleanup; the candidate unwinds through `compare`'s original
finally guards/copy cleanup before another version begins. It does not kill an
active subprocess or abandon its worker. Ordinary helper code is unchanged.

[AnyIO's worker cancellation API](https://anyio.readthedocs.io/en/stable/threads.html#reacting-to-cancellation-in-worker-threads)
supports cooperative checks inside workers. This motivates the prototype; actual
SDK cancellation and recovery, not documentation alone, must establish behavior.

Fixed four native cells: baseline active, candidate active, candidate queued,
baseline queued. Reuse the six-test Windows fixture with an explicit0.4-second
native setup delay. A real native marker must exist and no phase may have finished
before the actual cancellation notification. After cancellation error, use the
same session/server for complete before1/after0 recovery; retain all native outputs,
seven complete v3 observations/check, originals/modes and scratch removal. Inspect
actual phase starts/ends: canceled active baseline2 versus candidate1; queued
cancellation launches none, and both first/recovery comparisons run2 phases.
No timing threshold; cancellation-to-recovery includes the authored fixture delay
and recovery itself, not model efficiency. Existing SDK/client bounds remain.

[Server](results/tool-bridge-phase-cancel-01/server.py) and
[control](results/tool-bridge-phase-cancel-01/control.py) are isolated prototypes.
The launch-local serialized helper binding is wrapped; no global SDK patch.
Record every failure without overwriting prior results. No claim about arbitrary
thread interruption, larger batches, host deadlines, abrupt loss, SIGKILL or all8
performance. Inspect exception cleanup and incomplete-result handling before any
future adoption. The model approval gate remains a separate prerequisite.

## Executed contrast

Frozen source/execution **`915d7f81`**; current native helper from`026a8312`.
[Results](results/tool-bridge-phase-cancel-01/results.json),
[identities and runtime](results/tool-bridge-phase-cancel-01/identity.json), and
[control log](results/tool-bridge-phase-cancel-01/control-reading.txt).
Python3.11.6, MCP1.30.0 and AnyIO4.15.1. All four scheduled native cells finish;
no model calls, unplanned native reruns or source changes during this contrast.

| Arm / cancellation point | First request phases | Recovery phases | Cancel→recovery seconds |
| --- | --- | --- | ---: |
| Baseline / active | before, after | before, after | 1.988 |
| Candidate / active | before | before, after | 1.504 |
| Candidate / queued | before, after | before, after | 1.972 |
| Baseline / queued | before, after | before, after | 1.934 |

For queued cancellation, the first request is **not canceled**. The canceled
second request starts no phase; the table's final pair belongs to recovery.
Active candidate executes one fewer native process than active baseline: the
already-running before process finishes, cancellation is detected, original guards
and temporary-copy cleanup unwind, and after never starts. Both arms acknowledge
cancellation with a cancellation error, not a native verification result. Neither
promises immediate interruption or returns a synthetic successful comparison.

All four same-session recoveries return actual before1/after0 observations. Their
**eight reviewed native processes** each run the unchanged six tests with zero
skips and seven complete v3 argument records (**56 records**). Nested behavior is
actually `[(1,3)]` against `[(1,10)]` before and matching after; distinct input/result
identity is observed. Source guards and owned-copy cleanup pass. Actual starts and
ends match;15 native phase starts occur across first/recovery requests. The seven
non-recovery phases are retained lifecycle observations, not seven extra reviewed
repair outcomes. No double-response error, traceback or server-error line appears
in these four retained server logs. Session closure and awaited listener
termination finish; a separate numeric listener exit status was not retained.

The active recovery interval is lower in this one controlled comparison. Queued
candidate is slightly slower; do not average it away. Both timings include the
intentional0.4-second setup delay per phase and the entire subsequent recovery.
This establishes avoided work after cancellation, not normal-task latency, a
representative speed percentage, model tokens or an all-eight result.

## Decision and remaining work

Retain the phase-check mechanism as a supported **isolated native candidate**.
It is not installed, registered or promoted to ordinary skills. The model approval
failure remains unchanged, so no new model bridge trial follows. Cancellation
while Git/source preparation is running is only noticed at the next native phase;
an executing native process still uses its existing timeout/cleanup. This is not
an overall RPC deadline. Abrupt client loss, guard-error precedence during
cancellation, native timeout during cancellation, longer batches, cross-instance
concurrency and hard kills remain unverified for this candidate. A changed native
mechanism needs those relevant lifecycle checks before broader use; prior normal
controls must not be relabeled as complete lifecycle safety.

한국어: 실행 중 취소된 요청의 네이티브 비교를 기존2회에서 후보1회로 줄였다.
이미 실행 중인 프로세스의 정리를 기다린 뒤 다음 버전을 시작하지 않는다.
대기 중 취소에서는 두 방식 모두 취소된 요청을 실행하지 않았고, 같은 세션의
후속 비교4쌍·네이티브8회·실제 인자56개와 원본 보존·정리를 확인했다.
측정 시간에는 의도적인0.4초 지연과 후속 비교가 포함되며 대기 취소 후보는
조금 더 느렸다. 정상 작업의 토큰·시간 개선이나 전체8개 목표 달성으로 보지
않는다. 시제품으로만 보존하고 모델 승인 문제와 남은 종료 조건을 구분한다.
