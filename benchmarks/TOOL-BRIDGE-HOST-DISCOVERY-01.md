# Direct tool host discovery01 — 2026-09-27

Parent `7110af87`; unchanged [HTTP adapter](results/tool-bridge-http-exit-01/server.py)
identified by SHA-256 in [outcomes](results/tool-bridge-host-discovery-01/results.json).
This checkpoint contains **zero model runs** and changes none of the eight skill resources.

Actual Codex CLI0.157.1 generated its experimental app-server JSON schemas locally.
The owned Python3.11.6/MCP1.30.0 runtime launched the same loopback HTTP adapter
against a reused authored Receipt project; no independent task was introduced.
A separate actual `codex app-server` process received a scoped whole `mcp_servers`
table override with the owned endpoint, only `receipt_compare` enabled, and apps off.
No global registration, authentication change or configuration write was performed.

The client sent actual `initialize`, `initialized`, and `mcpServerStatus/list`
messages using the locally generated protocol. The returned target inventory
contained exactly one tool, its actual recipe input schema, and no discovery error.
Only that target and host user agent are retained; other host messages/inventory
are not exported. This verifies actual host tool discovery beyond the earlier
configuration-parser probe. It does **not** prove the host executed a native comparison.

The original project inventory and user/project configuration bytes and modes
matched before/after. The app-server exited0 and owned settled HTTP listener
exited−15 after SIGTERM. No active native worker existed in this discovery check;
this is not a new active-shutdown outcome. Executed [control](results/tool-bridge-host-discovery-01/control.py),
[reading log](results/tool-bridge-host-discovery-01/control-reading.txt) and
[source/protocol identities](results/tool-bridge-host-discovery-01/identity.json)
are retained. Temporary owned runtime logs were private; no provider/auth data
or initial host prompts were exported.

[HTTP cancellation01](TOOL-BRIDGE-HTTP-CANCELLATION-01.md) remains SDK-client proof
of active/queued cancellation followed by same-session recovery. It is not Codex
host cancellation proof. [HTTP exit01](TOOL-BRIDGE-HTTP-EXIT-01.md) retains cleanup
success with the interrupted RPC outcome unavailable, including the original
failed response expectation. [Forced stdio exit01](TOOL-BRIDGE-FORCED-EXIT-01.md)
retains the leaked native child and declined KeyboardInterrupt candidate.

No thread, turn, paid model or host-native tool call was started. Model tool
selection, startup/schema overhead, whole-task tokens/time, all-eight skill
benefit, abrupt client loss and cross-instance concurrency remain unverified.
The overall improvement objective remains unmet; this is not a released update.

한국어: 실제 Codex0.157.1 호스트가 임시 로컬 HTTP 도구와 입력 스키마를
발견했다. 모델 실행 없이 프로젝트 원본·설정 파일 보존과 검사 프로세스 종료를
확인했다. 호스트를 통한 실제 비교 실행·취소와 전체8개 스킬의 토큰·시간 절감은
검증하지 않았으며, 기존 종료·취소의 부정적 결과와 제한은 그대로 보존한다.
