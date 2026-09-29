# Direct tool host native01 — 2026-09-27

Parent `23235ae1`; unchanged [HTTP adapter](results/tool-bridge-http-exit-01/server.py)
identified in [outcomes](results/tool-bridge-host-native-01/results.json).
**Zero model runs**, unchanged eight skill resources and no efficiency adoption.
This follows [actual host discovery01](TOOL-BRIDGE-HOST-DISCOVERY-01.md).

The owned Python3.11.6/MCP1.30.0 runtime launches the same loopback server with
an authored, previously exposed Receipt project. Actual Codex0.157.1 app-server
receives a scoped MCP table override/apps-off setting, initializes and discovers
the one target tool. Using locally generated experimental protocol schemas,
the client starts one ephemeral thread, with no model turn, then sends two actual
`mcpServer/tool/call` requests to that thread's `receipt_compare` tool.
Only the target inventory/native results are exported; host instructions and
other provider inventory are not. No global registration/authentication change.

The final [executed control](results/tool-bridge-host-native-01/control.py) completes
both `bootstrap` and `module` invocation comparisons. Each returns native before1
and after0, six tests per process without skips, seven complete v2 actual assertion
argument records per process, copied-import verification and tree preservation.
Module startup provenance is explicitly ready. Four final native processes are
retained. Native exit1 is expected before-failure evidence; host tool response
is not an error and has no duplicate structured result.

Original project inventory and user/project configuration bytes and modes match
before/after; comparison scratch is gone after each call. Owned app-server exits0
and settled HTTP listener exits−15 after SIGTERM. This proves host-mediated native
execution, not simply a parsed configuration or an SDK-only client call.
[Final reading log](results/tool-bridge-host-native-01/final-control-reading.txt)
and [source/protocol identities](results/tool-bridge-host-native-01/identity.json)
are retained.

The first attempt fails in the **author's control**, which incorrectly requires
module-only `provenance_ready` in the bootstrap response. The original executed
[source](results/tool-bridge-host-native-01/first-control.py.gz),
[reading error](results/tool-bridge-host-native-01/first-control-reading.txt) and
[original identities/exit1](results/tool-bridge-host-native-01/first-attempt.json)
remain. That bootstrap call returned a native response before the control failed,
but the response was not exported before the assertion; its two processes are
not counted as reviewed final evidence. This is a corrected control, not a skill
fix or model retry. Prior prototype bootstrap/module format evidence was available;
the control's mistaken field assumption should have been avoided.

No model selected the tool or supplied the recipe. No whole-task input/output
cost, elapsed model task comparison, schema/startup overhead, all-eight benefit,
host cancellation, abrupt client disconnect or cross-instance concurrency is
verified. [HTTP cancellation01](TOOL-BRIDGE-HTTP-CANCELLATION-01.md) remains SDK-only;
[HTTP shutdown's unavailable interrupted RPC](TOOL-BRIDGE-HTTP-EXIT-01.md) and
[declined forced stdio exit](TOOL-BRIDGE-FORCED-EXIT-01.md) remain adverse evidence.
This checkpoint neither completes the overall improvement objective nor ships
the adapter as a general update.

한국어: 실제 Codex 호스트를 통해 두 실행 방식의 수정 전 실패·수정 후 통과,
각6개 테스트·7개 실제 인자 관찰과 가져오기·원본·설정 보존·정리를 확인했다.
검사 코드의 최초 필드 오류도 보존했다. 모델이 도구를 선택한 실험이 아니므로
토큰·시간 절감이나 전체8개 스킬의 개선을 주장하지 않는다.
