# Solver serial channel01 — 2026-09-27

Parent `ab80dbe8`; actual interactive host→guest command transport, zero models or
selected issue tests. This is a prototype channel, not a deployed model/MCP tool.

Reuse the [guest child runtime](SOLVER-CHILD-EXECUTION-01.md): RAM-only source/
Python, guest binfmt/devtmpfs, one Rosetta translation share, no host data shares,
network or storage devices. Swift forwards host stdin bytes to the guest serial
console. After initialization, the guest switches its console to raw/no-echo and
starts the Python command agent. Host waits for the exact ready line before sending
JSON requests; guest executes `/bin/busybox sh -c` with the requested guest cwd.
There is no host shell fallback. Child stdin is `/dev/null`, preserving the request
stream for the agent.

[Exact agent](results/solver-serial-channel-01/agent.py) captures binary stdout/stderr,
exit code and timeout state. A selector drains both pipes, retains the first4096
bytes each and counts all bytes read, explicitly marking truncation. Output travels
as base64 JSON with request ID. Commands run in owned sessions; a request deadline
kills the process group, followed by bounded drain/wait. Remaining live parent is
killed in cleanup. Request timeout is at most10 seconds. Inherited-pipe descendant
cleanup, hostile guest console spoofing, input-size limits, parallel requests and
durable file export are not verified; this is not a finished production tool.

The [first controller/source](results/solver-serial-channel-01/first-control.py)
fails when a queued initialization line reaches the agent's JSON stream, producing
JSONDecodeError/id-null before the expected request response. The controller rejects
the response and kills the VM process group in cleanup. Initial agent/Swift and
[complete collected output](results/solver-serial-channel-01/first-guest.txt) remain
retained. No valid command outcome is inferred from that failed attempt.

The separate corrected input removes the queued shell poweroff line; explicit
shutdown is handled by the agent, which announces stop then powers off the guest.
Blank protocol lines are ignored. The host parser also processes buffered complete
lines before waiting for another read, so shutdown observations do not depend on
serial packet boundaries. Original input hashes remain separate from second hashes.

[Actual second controller](results/solver-serial-channel-01/control.py) completes six
sequential request checks on the real VM:

| Request | Observed result |
| --- | --- |
| Guest uname |Exit0, exact `Linux\n`. |
| Deliberate failure |Exit7, stdout bytes00ff, stderr `failure`. |
| Missing `/Users` cwd |FileNotFoundError, no command execution fallback. |
| Controlled timeout |Timed out, exit−9 after process-group kill. |
| Long stdout/stderr |20,000 bytes each drained;4096 each retained; both truncated=true. |
| Recovery |Exit0, exact `recovered` after prior failure/error/timeout/truncation. |

[Retained response evidence](results/solver-serial-channel-01/result.json) includes
actual base64 bytes and counters, not just summary booleans. Guest agent stop,
normal VM shutdown and executable0 are observed. [Complete collected console](results/solver-serial-channel-01/guest.txt)
and both Swift configurations, agent/control sources and initramfs hashes are
retained. VM deadline45 seconds; host observation55 seconds plus bounded cleanup.
Cpio30 seconds; staging/compression/compilation/signing lack an independent whole-
attempt deadline and completed. Both host VM processes are terminal. No new disk,
network service, host account configuration or personal MCP installation.

This supplies real serial request/response semantics for a future solver adapter.
It does not prove model tool availability/selection, final isolation configuration,
full native issue grading, role quality or joint whole-task token/time reduction.
Output caps are an observed transport feature, not measured model token savings.
Source-archive portability is not tested here; the controller takes explicit frozen
VM inputs and needs the installed Mac virtualization platform. Skills/README/
featured/site performance claims remain unchanged. Next connect the channel through
an isolated model-facing adapter with actual execution evidence and preserve all
outstanding fixed-cohort grading limits.

한국어: 실제 serial 입력으로 게스트 명령을 실행하고 종료 코드·바이너리 출력·
시간 초과·잘림 상태를 반환했다. 실패·오류·시간 초과 뒤 다음 요청도 정상 처리했다.
최초 시작 입력 혼선 실패는 보존했고 명시적 종료로 VM을 정상 종료했다. 모델
연결·실제 이슈 평가·전체 품질·토큰·속도 개선 증거는 아직 아니다.
