# Direct tool concurrency01 — 2026-09-27

Parent `6c212555`; separate local SDK adapter candidate, **zero models or ordinary
skill changes**. [Native prototype01](TOOL-BRIDGE-NATIVE-PROTOTYPE-01.md) verified
serial calls but left concurrent ownership unverified.

[Controlled overlap source](results/tool-bridge-concurrency-01/control.py),
[serialized adapter](results/tool-bridge-concurrency-01/server.py),
[actual original results](results/tool-bridge-concurrency-01/results.json) and
[SDK log](results/tool-bridge-concurrency-01/control-reading.txt) retained.
An unchanged six-test native fixture adds only a controlled setUpModule marker and
0.4-second delay inside each disposable native copy. Submit the second MCP request
only after the first native copy's actual marker exists; no speculative sleep-only
start or scheduler mock. Reuse exact source/test/runtime choices in both conditions.

Previous adapter: overlapping requests produce actual Project tree changed
errors because source guard inventories include the other request's temporary
copy. All call outcomes retained, not recast as repair proof. Both requests settle,
original file bytes/modes/Git inventory match and owned scratch is removed.
No assertion comparison result is inferred for an errored call.

Candidate changes only adapter admission: an async project gate wraps the entire
non-abandoning native helper worker. Two admitted overlapping SDK requests both
finish observed with complete current six-test suites, native before1/after0,
seven actual primitive argument records per native process and complete provenance,
source guard and cleanup. Four successful candidate native processes. No duplicate
structured output or refreshed/cached evidence replaces execution. Individual
native before failures remain valid comparison observations, not MCP errors.

This is a demonstrated interaction repair, **not whole-task savings**. Serialization
can increase queue latency. Gate covers one server instance's launch-fixed root;
it is not a filesystem lock across other server instances, user commands or agents,
not an atomic snapshot and not a sandbox. Cancellation of queued/active work,
disconnection/shutdown and actual Codex-host connection remain unverified. Do not
ship/benchmark the adapter as lifecycle-ready merely because overlap now passes.
Earlier ordinary skill release/model measurements keep their exact resources.
All8 still needs all roles and lower whole input+output plus faster work.

한국어: 실제 네이티브 시작 후 요청을 겹쳐 기존 시제품의 원본 변경 감지 오류를
재현했다. 프로젝트별 직렬화 후에는 두 비교 모두 실제1/0·전체6개 검사·원본
보존·정리를 확인했다. 대기 시간이 늘 수 있으므로 토큰·시간 절감으로 표현하지
않으며 여러 서버 인스턴스·취소·종료·Codex 연결·전체8개 개선은 미검증이다.
