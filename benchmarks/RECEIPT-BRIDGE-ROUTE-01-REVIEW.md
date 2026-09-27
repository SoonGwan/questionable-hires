# Receipt bridge route01 — decline under retained policy, 2026-09-28

Source **`d5643767`**, candidate/execution **`2708692d`**.
[Protocol](RECEIPT-BRIDGE-ROUTE-01-PROTOCOL.md),
[all four attempts](results/receipt-bridge-route-01/run.json),
[costs](results/receipt-bridge-route-01/comparison.json),
[original native/preservation review](results/receipt-bridge-route-01/original-review.json).

**Do not adopt or repeat this unchanged configuration.** Both candidate models
resolve the exact tool and emit a call, but the host rejects both before the server
executes anything. Native verification is completed through fallback routes.
The whole-task costs increase in both pairs. Ordinary skills, personal copies,
downloads, featured claims and hosted release are unchanged.

| Task | CLI tokens | Bridge tokens | CLI seconds | Bridge CLI seconds | Bridge + lifecycle seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Single version comparison | 71,806 | 104,784 | 44.324 | 48.825 | 49.343 |
| Multiple version comparison | 75,099 | 77,485 | 52.120 | 66.791 | 67.403 |
| Sum | 146,905 | 182,269 | 96.444 | 115.616 | 116.746 |

Whole-task tokens **+24.07%**, CLI elapsed **+19.88%**, CLI plus bridge startup/
shutdown **+21.05%**. Lifecycle time excludes author export/inventory review.
Responses5→7 on single and5→5 on multiple. Per-response counters reconcile with
final CLI usage, cached input counted once. All four scheduled sessions complete
without model timeout, limit, replacement or retry. The failed tool calls and
fallback costs remain charged. These exposed related tasks, n=1, shared host/cache,
balanced order and unequal implementation work are not a causal or all-eight result.

## Actual gate, not tool execution

Each candidate emits one `qh_receipt_bridge_01.receipt_compare` request. Both fail:

> MCP tool call requires approval, but approval policy is never

Each owned server receives one `ListToolsRequest` and zero `CallToolRequest`.
[Reading logs and hashes](results/receipt-bridge-route-01/server-log-identity.json)
corroborate the host-side failure. Settled listeners exit−15. Resolving/attempting
a named tool is now observed; approved model tool execution is **not** observed.
This is not a helper assertion failure, a delivered incomplete comparison, or proof
that the full schema was initially injected. No approval settings were changed and
no blocked request was retried through the bridge.

The [current-helper preflight](results/receipt-bridge-route-01-setup/results.json)
had made actual host API calls without a model turn: both native invocation styles
returned before1/after0, six tests and seven complete v3 records each, preserving
originals/configuration and removing scratch. That administrative host API path
**does not exercise the model approval gate**. The preflight therefore supported
native compatibility, not permission for model-issued calls. Five Git-free synthetic
runner controls passed separately, including retaining normal rules. Neither is
model efficiency evidence or universal lifecycle certification.

The single candidate also requested a native timeout60 while the host tool timeout
is40. Because approval blocked it, this run establishes no active-call deadline
compatibility. Historical SDK cancellation and bounded native examples must not
be generalized to every timeout value or longer batch.

## Original native fallback evidence

CLI single, CLI multiple and bridge single use the unchanged native Receipt helper.
They produce seven processes with complete v3 assertion observations. Bridge
multiple reads the guide but authors a temporary stdlib comparison instead: three
real unittest processes, a same-process profile hook on actual assertion frames,
copy import/test hashes, full revision IDs and explicit process exits. Its hook
observes these primitive fixture values; it is not validated as a general codec.
The different orchestration and recovery work remain visible.

Across all four original sessions: **ten native processes**, each running the same
six current tests without skips, and **70 actual argument observations**. Single
comparisons exit1/0: before nested windows yield `[(1,3)]` against `[(1,10)]`;
after they match. Multiple comparisons exit1/1/0: oldest also fails touching
windows, middle fixes touching but still fails nesting, current passes both.
Chain/disjoint/empty/input-preservation controls pass across versions. Actual
identity assertions observe distinct result/source objects. Source/test hashes,
copy-local imports, original bytes/modes, HEAD, captured indexes and installed
resources match; owned scratch is removed and no project files remain added.
Those final inventories do not prove every transient or external effect absent.

### Original output recovery

Bridge multiple's CLI item5 begins at the first process's provenance line, omitting
the first revision/command/source prefix. Two author review assertions requiring
three revision headers failed; changing a leading-newline assumption did not fix
the missing data. The same stored session's paired call34/output37 supplies the
complete9,086-character output and exit0. Its8,541-character CLI aggregate is an
exact suffix. [Recovery identity](results/receipt-bridge-route-01/bridge/windows-multiple--skill--1/native-output-recovery.json)
and [complete original output](results/receipt-bridge-route-01/bridge/windows-multiple--skill--1/native-tool-output-line-37.txt)
are retained alongside the unchanged aggregate. No model or native check was rerun.
The corrected review checks every actual value and source identity against that
original response; later execution is not used to fill the gap.

## Decision

No further model bridge trials under these unchanged approval settings. A future
bridge evaluation needs a legitimately authorized, policy-compatible call path and
verified deadline/cleanup contracts first. Do not remove safeguards, change tool
annotations to misrepresent writes, or infer model-call permission from direct
administrative API success. CLI fallback verification remains valid within the
authorized task, but does not demonstrate the bridge's intended efficiency.
All-eight quality/token/time improvement is still unproven.

한국어: 직접 도구 호출 경로를 안내하자 두 모델 모두 호출을 시도했으나, 호스트가
승인 필요·승인 정책 never 사유로 실행 전에 막았다. 서버에서는 도구 조회만
관찰됐고 실제 비교 호출은0회다. 설정을 바꾸거나 요청을 재시도하지 않았다.
대체 CLI/임시 표준 라이브러리 비교에서10개 네이티브 프로세스·70개 실제 인자
관찰과 원본 보존은 확인했다. 합계 토큰24.07%, 서버 시작·종료 포함 시간21.05%
증가로 후보를 채택하지 않는다. 직접 호스트 API 사전 검사는 모델 승인 경로를
검사하지 않았으며, 같은 승인 설정으로 추가 모델 실험을 반복하지 않는다.
