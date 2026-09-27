# Solver MCP HTTP01 — 2026-09-27

Parent `3607ec91`, prospective transport candidate, **zero model calls and selected
issue tests**. [Actual model catalog01](SOLVER-MODEL-CATALOG-01.md) found no guest
tool in its code-mode pool despite native stdio registration. This candidate reuses
the HTTP transport approach from `run_receipt_tool_bridge_01.py`; it does not
assume transport explains that observation or repeat the original model task.

[Separate server](results/solver-mcp-http-01/server.py) preserves lifecycle01's
Guest class exactly (AST equality checked). It adds an explicit transport choice,
stdio by default, and validated port1024–65535. FastMCP binds only127.0.0.1 and uses
the owned selected port for streamable HTTP at `/mcp`. Guest execution, return
semantics, schema and honest mutating/destructive tool annotations are unchanged.
No host shell fallback, host data share, personal config or approval override.
The original stdio candidate and evidence remain frozen; no new stdio run is claimed.

[Frozen native launch](results/solver-mcp-http-01/launch.json) records source hash,
owned ephemeral URL, interpreter and boundaries before launch. [SDK control](results/solver-mcp-http-01/sdk-control.py)
reuses the original four commands and assertions, replacing only the stdio client
boundary with `streamable_http_client`. HTTP initialization and tool listing succeed.
[Native results](results/solver-mcp-http-01/result.json) retain actual Linux output,
exit7 with stdout `failed` and MCP isError false, cwd `/Users` FileNotFoundError with
isError true, then stdout `recovered`. Command failure is not renamed tool success.

[Delivery](results/solver-mcp-http-01/delivery.json): SDK0, server−2 after the owned
coordinator's SIGINT,8.887s. The signed server exit is retained rather than reported
as natural exit0. [Complete guest console](results/solver-mcp-http-01/guest.log)
contains readiness, four responses and graceful guest stop. The exact owned probe
is absent and HTTP port closed after cleanup; no forced cleanup was required.
Startup cap20s, SDK cap40s and server cleanup10s. The existing frozen VM has its
own45-second deadline. Raw HTTP/server logs remain private, separate from guest
console and public SDK output. No authentication/private config data exported.

This verifies native HTTP command delivery, not model catalog inclusion, model
approval, enforced absence of host tools, selected regressions, skill quality or
whole-task resource savings. The next observation must inspect this candidate's
actual model tool catalog before attempting any issue-solving comparison. The
previous host-workspace receipt approval rejection remains adverse; transport
support does not justify changing annotations or bypassing approval.
Ordinary skills, README onboarding, featured benchmark and public site unchanged.

한국어: 별도 HTTP 후보에서 기존 게스트 클래스와 네 가지 SDK 검사를 유지했다.
실제 Linux·실패 종료코드·잘못된 경로·후속 복구를 모두 확인했다. 작성자 SIGINT
종료코드−2를 보존하며 게스트 정상 종료·프로세스 제거·포트 닫힘을 확인했다.
모델 호출0회로 모델 도구 노출이나 품질·토큰·속도 개선 증거는 아직 아니다.
