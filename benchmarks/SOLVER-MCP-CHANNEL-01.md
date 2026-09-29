# Solver MCP channel01 — 2026-09-27

Parent `2fa70d44`; real MCP protocol calls to the guest channel, models0, selected
issue tests0. This is an experimental adapter, not current model availability or
an adopted skill optimization.

Reuse the existing owned mcp1.30.0 SDK/runtime from the retained tool-bridge work
and the frozen [serial-channel02 VM](SOLVER-SERIAL-CHANNEL-01.md). No package install,
personal MCP registration, host configuration change or new HTTP/network service.
The adapter uses stdio transport: SDK client initializes a real FastMCP server,
lists its tool and calls it. The server boots only the supplied owned VM executable;
command strings travel as serial JSON to the guest, never to a host shell.

[Server](results/solver-mcp-channel-01/server.py) exposes `guest_command` with honest
annotations: readOnly=false, destructive=true, idempotent=false, openWorld=false.
Arbitrary authorized commands may change/delete guest files. We do not relabel the
tool readonly, fake approval metadata or change a global approval setting. Native
SDK invocation does not exercise Codex automatic approval review or prove an actual
model is allowed to use this tool. The prior Receipt bridge approval limits remain
historical; this does not claim they are repaired.

Tool arguments are strict bounded strings and integer timeout1–10 seconds. The
serial agent preserves actual exits, timeout state, base64 binary streams and
truncation flags. Host adapter serializes calls under a lock and checks response IDs.
An observed nonzero command exit stays a returned execution result, requiring the
caller to inspect its exit; channel/launch errors are MCP tool errors. No exit7
is converted to command success. An error does not silently invoke a host fallback.

[Actual client control](results/solver-mcp-channel-01/control.py) verifies initialize,
list_tools, complete annotation values and four call_tool round trips:
guest Linux stdout, deliberate exit7/stdout`failed`, unavailable `/Users` cwd as
FileNotFoundError/isError=true, and recovery/stdout`recovered` after that error.
[Retained tool results](results/solver-mcp-channel-01/result.json) contain the actual
SDK tool schema/annotations and response values. Earlier serial-only timeout/binary/
truncation controls remain separate evidence, not new MCP observations.

Client closure triggers guest shutdown. [Delivery check](results/solver-mcp-channel-01/delivery-check.json)
records both stop markers, exact owned VM process absence, SDK version and source/
console hashes. [Complete guest console](results/solver-mcp-channel-01/guest.txt)
and SDK events remain retained. Guest has one Rosetta translation share, no arbitrary
host data shares/network/storage, with original all8 source/RAM runtime inputs.
Neither grader/gold nor selected native test data is added.

The native client has40-second outer async timeout, VM45-second deadline, server
startup observation20 seconds, per-request timeout+3 seconds for response delivery,
and bounded shutdown/kill. Constructor-failure cleanup, cancellation/concurrency,
malicious console frames and source-archive portability are not verified; this is
not a production-ready endpoint. A finalized model launch must also prove host
tools cannot bypass the guest boundary, actual tool exposure/approval behavior,
output artifact transfer and fixed-cohort grading readiness. None is implied by
these direct SDK calls. Skills/README/featured/site performance claims remain
unchanged; all8 quality and whole-task token/time objectives are unmet.

한국어: 기존 SDK로 실제 MCP 초기화·도구 목록·게스트 명령 호출4개를 확인했다.
변경 가능·파괴 가능이라는 정확한 도구 메타데이터를 유지했고, 종료7과 채널
오류를 구분한 뒤 복구도 확인했다. 개인 MCP 설정·승인 설정은 바꾸지 않았다.
실제 모델 노출·승인·호스트 도구 차단·이슈 평가·전체 품질·토큰·속도 비교는
아직 검증하지 않았으며, VM 종료와 프로세스 부재는 확인했다.
