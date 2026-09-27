# Direct tool cancellation01 — 2026-09-27

Parent `97f1a760`; local SDK adapter repair, **zero models/ordinary skill changes**.
[Concurrency01](TOOL-BRIDGE-CONCURRENCY-01.md) fixed overlapping source guards;
[native prototype01](TOOL-BRIDGE-NATIVE-PROTOTYPE-01.md) and
[parser feasibility01](TOOL-BRIDGE-FEASIBILITY-01.md) remain separately dated.

Actual cancellation revealed a second lifecycle bug: SDK sends cancellation error
immediately, but non-abandoning helper work subsequently returns normally. The
request handler attempts another response and raises `Request already responded
to`, terminating the server; the next tool request cannot recover.

The first [control](results/tool-bridge-cancellation-01/initial-control.py) stays
pending despite no live native test processes. Exact owned control was interrupted
with SIGINT, confirmed exit130; [reading log](results/tool-bridge-cancellation-01/initial-interrupted-reading.txt)
retained. No passing cancellation/cleanup verdict follows from that interruption.
A diagnostic authoring attempt has an IndentationError before SDK execution;
[error](results/tool-bridge-cancellation-01/diagnostic-authoring-failure.txt) retained.
Corrected [diagnostic control](results/tool-bridge-cancellation-01/diagnostic-failed-control.py)
adds stage markers and a five-second client read timeout. Its original
[terminal error](results/tool-bridge-cancellation-01/diagnostic-failure-reading.txt)
shows cancellation acknowledged, next request submitted, double-response assertion
and recovery timeout. This distinguishes request recovery from a mere transport
close wait; earlier pending execution is not retroactively marked complete.

Candidate [server](results/tool-bridge-cancellation-01/server.py) adds only a
cancellation checkpoint after non-abandoning native cleanup, inside the project
gate. Pending cancellation propagates before a normal response; gate releases
on unwind. No SDK patch, abandoned worker, rewritten native assertions or cached
successful result. SDK/runtime dependency identity remains in native prototype01.

Final [control](results/tool-bridge-cancellation-01/control.py) sends actual MCP
cancellation notifications for active and queued requests, after a native started
marker confirms active work. Both receive cancellation errors, then the same
server/session performs complete native recovery before1/after0 under unchanged
six-test assertions. Two recovery pairs/four native processes explicitly retained
in [original results](results/tool-bridge-cancellation-01/results.json); full imports,
observed primitive arguments, source guards and scratch cleanup preserved.
Original file/mode/Git inventories match after recovery and graceful transport
close. [Final SDK stage log](results/tool-bridge-cancellation-01/fixed-control-reading.txt)
records both session/transport exits. These are new runs, not rescored failures.

Cancellation acknowledgement is **not immediate native interruption/cleanup**;
active helper work may finish before gate release. Acknowledged cancellation has
no native success/repair proof. Queued first work and active canceled work are not
added to the two explicitly retained recovery pairs as reviewed native outcomes.
Bounded normal graceful close is tested here; abrupt disconnect/forced shutdown,
cross-server ownership and actual Codex host/model behavior remain unverified.
No token/time/all8 advantage or shipped bridge follows. Next gates are disconnect
and host tool discovery, then a frozen whole-task comparison counting all schema,
setup and failures. Existing negative model costs remain unchanged.

한국어: 실행 중 취소 후 두 번째 응답을 시도해 서버가 종료되는 오류를 실제로
확인했다. 네이티브 정리 후 취소를 전달하도록 수정해 실행 중·대기 중 취소와
같은 서버의 후속 실제1/0 비교·원본 보존·정상 종료가 통과했다. 초기 중단·검사
작성 오류·원본 서버 오류도 보존한다. 즉시 작업 중단이나 강제 연결 종료,
Codex 연결·전체 토큰·시간 절감·8개 개선을 검증한 것은 아니다.
