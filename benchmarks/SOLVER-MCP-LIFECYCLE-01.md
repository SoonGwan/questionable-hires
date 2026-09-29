# Solver MCP lifecycle01 — 2026-09-27

Parent `e41e9e98`; prospective guest adapter cleanup repair, zero model calls or
selected issue tests. Original [MCP channel01](SOLVER-MCP-CHANNEL-01.md) source and
four-call evidence stay frozen; the separate candidate is retained here.

The previous Guest constructor starts a process before opening its exclusive log
and waits for readiness without an exception cleanup path. Response timeout or
wrong ID also leaves the process/channel open; a later request could encounter
remaining stale output. The candidate opens its log before launch, owns startup
cleanup, and makes protocol/transport exceptions terminal for that channel. It
kills/reaps the owned process group, closes selectors/pipes/log, and rejects further
requests on the closed channel. It does not silently restart/retry a cell. Normal
close is serialized with requests and idempotent.

[Exact class control](results/solver-mcp-lifecycle-01/control.py) extracts each actual
Guest AST class, without importing MCP or the server main, and compiles it with
standard-library dependencies. Synthetic native Python subprocesses emulate the
serial peer: never ready, wrong ID, never responding, and normal response/shutdown.
They do not execute commands, use a VM or provide model evidence. Both arms receive
the same bounded1-second observation cap; production startup20-second and response
timeout+3-second values are not changed to fit the test.

[Observed previous/candidate results](results/solver-mcp-lifecycle-01/lifecycle.json):
previous process remains live after each of the three failures; candidate stops
each before author cleanup and rejects the next request. Both normal cases shut
down. Candidate repeated close also succeeds. The author control then explicitly
kills/reaps previous leaked owned processes, preserving the before-cleanup observation.
[Git-free copied controls](results/solver-mcp-lifecycle-01/git-free.json) reproduce
these scoped results using explicit previous/candidate sources, no repository history
or local-run inputs; outer coordinator15 seconds. These are process/pipe controls,
not native virtual-machine failure simulations or a new benchmark-quality score.

The initial0.2-second author cap incorrectly interrupts normal interpreter startup
in both arms. Its first assertion failure, incomplete output and exact control
source remain in the `initial-*` artifacts. A later diagnostic observed empty
normal-case logs, motivating the1-second control correction. No full initial vector
was exported; do not reconstruct it as a scored result. This author test defect does
not relabel the old SDK/VM success or the original model measurements.

[Real SDK control](results/solver-mcp-lifecycle-01/sdk-control.py) separately repeats
the four original native MCP calls on the candidate with the same frozen serial02
VM input. [Actual results](results/solver-mcp-lifecycle-01/result.json) retain honest
mutating/destructive annotations, guest Linux output, exit7, cwd error and recovery.
[Delivery evidence](results/solver-mcp-lifecycle-01/sdk-delivery.json) identifies the
candidate source, complete console, observed guest stop and exact VM process absence.
This real SDK control is distinct from the synthetic failure tests; actual VM startup
and request timeouts are not injected here. Model approval/exposure is not exercised.

No host configuration, personal MCP registration, network service or ordinary skill
changes. Candidate preserves the guest-only command path, no host shell fallback,
no host data directory shares, one Rosetta share. Cancellation/concurrent requests,
abrupt server termination and malicious-frame behavior still need their own evidence.
Native issue grading/tool exposure/host-tool exclusion and all8 quality/lower
whole-task tokens/faster completion remain unmet. README/featured/site claims stay
unchanged; fail-closed cleanup is not measured model efficiency.

한국어: 기존 도구의 시작·응답 실패 후 프로세스 잔류를 합성 실제 프로세스로
재현했고, 별도 수정본에서는 정리와 후속 요청 차단을 확인했다. 정상·반복 종료,
Git 없는 복사본, 실제 VM의 MCP4회 호출은 각각 검증했다. 최초 검사 예산 오류도
보존한다. 모델 승인·강제 서버 종료·전체 이슈 및 품질·토큰·속도 비교는 미완료다.
