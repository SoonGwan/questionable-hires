# Solver model connectivity01 — 2026-09-27

Parent `0d8ce3d4`, adapter from [lifecycle01](SOLVER-MCP-LIFECYCLE-01.md).
One scheduled Codex `gpt-6-astra` medium-effort connectivity attempt, with no
issue statement, grading inputs, patch task or performance comparison. This is
an original model observation, separate from the earlier successful native SDK
calls. Ordinary skills, README capability descriptions and featured data unchanged.

[Frozen launch](results/solver-model-connectivity-01/launch.json) identifies the
server hash, exact scoped configuration and harmless single Linux uname request.
The owned project directory is empty. Personal configuration and tool annotations
were not changed; no approval bypass or host fallback was requested.

[Preflight observations](results/solver-model-connectivity-01/preflight.json):
`features list` rejects `--strict-config`, which is supported by `exec`. Without
that option, four requested features report false, but `unified_exec` reports true
despite both the disable flag and explicit false configuration. The author
all-five-disabled assertion failed before any model or VM launch. The subsequent
connectivity-only manifest explicitly retains this unresolved limitation. Feature
flags are not evidence of the model's actual complete tool catalog or isolation.
The [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents shell features and MCP allowlists; it does not establish why this local
CLI reports this combination. No private configuration/profile content is exported.

[Terminal record](results/solver-model-connectivity-01/terminal.json): CLI exit0,
12.681 seconds, outer90-second timeout not reached. [Sanitized original events and
usage](results/solver-model-connectivity-01/result.json) retain the model's report
that `qh_guest guest_command` was unavailable. That CLI stream records no tool calls;
the original rollout review below recovers one omitted code-mode lookup. There are
zero guest command calls, rather than zero calls of every tool.
Input22,447 + output127 = **22,574 total tokens**; cached input19,840 is already
included, not added again. CLI exit0 means the turn ended, not tool success.

[Complete guest console](results/solver-model-connectivity-01/guest.log) observes
`QH_AGENT_READY`, no command responses and no graceful stop marker. The exact owned
probe process is absent after CLI termination. This does not exercise cancellation
or establish graceful guest cleanup. No OS/command exit code was returned to the
model. Its unavailable-tool statement does not by itself explain actual catalog
exposure; no automatic approval rejection was observed in retained CLI events.
Raw CLI/session messages remain private; only benign answer/usage/console records
are exported. No favorable retry replaces this attempt.

No connectivity, enforced host-tool exclusion, native issue grading, skill quality,
whole-task savings or faster-completion claim follows. The next prerequisite is
actual tool exposure evidence, rather than another unchanged model attempt.
The dated [previous decision index](CANDIDATE-HISTORY-2026-09-27-BEFORE-SOLVER-MODEL-CONNECTIVITY-01.md)
preserves the preceding state.

## Original rollout review and native inventory — 2026-09-27

Follow-up parent `548898e7`; no additional model attempt. The first report at
`2a9f6e5b` inferred zero calls from the CLI JSON stream, which omitted the original
custom tool events. [Exact original session review](results/solver-model-connectivity-01/session-tool-review.json)
recovers **one `exec` call** searching `ALL_TOOLS` by a regex requiring both
`qh_guest` and `guest_command`. Its output says unavailable. This changes the
all-tools count, not the guest-command count, usage or terminal result; the first
`result.json` stays frozen as the initial CLI-derived observation. The regex result
cannot distinguish catalog exclusion from a tool identifier lacking the expected
server name. It is not a full inventory. Private instructions and metadata are omitted.

The existing `app_server_capture_probe.py` Connection is reused for a separate
native `initialize` / `mcpServerStatus/list` request with the same scoped flags,
without a thread or model. The exclusive guest log path is changed to an owned new
directory; `--strict-config` belongs to the exec invocation and is not used for this
app-server command. [Owned server inventory](results/solver-model-connectivity-01/native-inventory.json)
returns `qh_guest` / `guest_command`, actual schema and honest mutating/destructive
annotations, with no tool error. Other server inventories and raw RPC messages are
not exported. [Complete console](results/solver-model-connectivity-01/native-inventory-guest.log)
observes readiness, zero guest responses and no graceful stop; exact probe absence
is checked after app-server close. Native registration succeeds, but does not prove
what code-mode `ALL_TOOLS` exposes to this model. The next distinct observation
should inspect guest-tool names in that actual catalog, without re-solving a task.

한국어: 최초 실제 모델 연결 검사는 입력·출력22,574토큰을 사용했지만 도구
호출은0회였다. 게스트 준비는 확인됐으나 모델은 도구를 사용할 수 없다고 응답했다.
종료코드0을 연결 성공으로 취급하지 않으며, 도구 노출 원인은 미확인이다.
CLI 설정에서 셸은 비활성화됐지만 unified_exec는 활성 상태로 보고됐다.
호스트 도구 격리·정상 게스트 종료·전체 과제 토큰 절감 증거는 아니다.
불리한 원본 실행과 최초 사전 검사 오류를 보존하며 같은 조건으로 재시도하지 않는다.

한국어 후속 정정: CLI 요약에서 누락된 원본 `exec` 검색 호출1회를 복구했다.
게스트 명령 호출은0회이며 토큰·종료 결과는 그대로다. 네이티브 서버 조회에서는
`qh_guest`의 `guest_command` 등록을 확인했다. 모델의 검색 정규식은 서버 이름을
요구하므로 실제 목록에서 이름이 달라진 경우와 도구 제외를 구별하지 못한다.
추가 모델 실행 없이 증거를 보완했으며, 기존 CLI 기반 관측 파일도 보존했다.
