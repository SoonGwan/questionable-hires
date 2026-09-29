# Direct tool forced exit01 — 2026-09-27

Parent `b2a593da`; **declined lifecycle candidates, zero models/ordinary skill
changes**. Cancellation01's normal recovery remains valid for its scoped
resource; it does not establish forced termination safety.

[Baseline control](results/tool-bridge-forced-exit-01/baseline-control.py) actually
initializes the stdio protocol, starts a real native unittest child and confirms
its PID marker before sending SIGTERM to the owned server. [Actual baseline](results/tool-bridge-forced-exit-01/baseline-result.json):server exits−15 while the
native child is still live and owned scratch remains. No native result/repair
proof returned. Author then terminates only that recorded native process group,
confirms terminal state and removes the owned project. This intervention is not
adapter success; baseline declined.

[Candidate](results/tool-bridge-forced-exit-01/server.py) converts SIGTERM to normal
Python interruption rather than immediate process termination. [Candidate control](results/tool-bridge-forced-exit-01/control.py) does not pass: waiting5seconds for
server exit times out, and [server stderr](results/tool-bridge-forced-exit-01/server-reading.txt)
reports fatal buffered-stdin lock failure during interpreter shutdown. [Actual
failure](results/tool-bridge-forced-exit-01/candidate-failure-reading.txt) and
[negative metadata/hashes](results/tool-bridge-forced-exit-01/candidate-result.json)
preserved. Finally again confirms controlled child terminal; owned project is
removed by author. No candidate success JSON was produced; stale baseline output
is retained only under baseline-result to avoid mislabeling it as candidate output.

Do not ship/register/benchmark this bridge as lifecycle-ready. Earlier active /
queued cancellation and serial/concurrent native results keep their own hashes
and scopes; these adverse outcomes are not rescored or replaced with normal close.
The default SDK stdio reader/thread shutdown now needs a different lifecycle
mechanism or supported SDK transport; raising KeyboardInterrupt is not adopted.
No SDK/global package/config/ordinary skill modification follows from this failed
candidate. SIGKILL/unrelated crashes, longer native batches and other platforms
remain unverified; no universal crash cleanup guarantee is possible from these
controls. All8 quality/token/time objective remains unmet, but this eliminates
an unsafe direct-tool delivery path without hiding its failed attempts.

한국어: 실제 네이티브 시작 후 서버 SIGTERM에서 자식 프로세스와 임시 복사본
누수를 확인했다. 신호를 일반 인터럽트로 바꾸는 후보도 종료 대기 초과와 표준입력
버퍼 잠금 오류로 실패해 채택하지 않는다. 자식과 프로젝트는 작성자가 따로
정리했으며 자동 정리 성공으로 표시하지 않는다. 원본 실패를 보존하고 연결
시제품의 배포·효율 비교는 보류하며 전체8개 목표는 계속 미완료다.
