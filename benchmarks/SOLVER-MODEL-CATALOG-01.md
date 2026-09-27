# Solver model catalog01 — 2026-09-27

Parent `7225e0f8`; one original `gpt-6-astra` medium-effort metadata-only attempt.
It does not repeat the failed uname task or solve an issue. The preceding native
inventory registered the owned stdio MCP guest tool, while the original model's
server-name regex could not distinguish exclusion from identifier translation.
[Original review](SOLVER-MODEL-CONNECTIVITY-01.md#original-rollout-review-and-native-inventory--2026-09-27)
retains that distinction and the CLI-omitted exec call.

[Frozen manifest](results/solver-model-catalog-01/launch.json) preserves the exact
configuration, source hash and distinct prompt. The model is asked to invoke exec
once, inspect ALL_TOOLS count, and match tool names or descriptions against the
server name, command name or distinctive owned guest description. It must not
invoke the guest or other tools. Personal configuration and annotations unchanged;
the unresolved unified_exec feature observation remains explicit.

[Actual original rollout events](results/solver-model-catalog-01/result.json)
record exactly one exec lookup and output **catalog_count13, matches[]**. This
broader lookup finds neither the expected command/server identifier nor the
distinctive owned guest description. The original model-visible code-mode pool
does not contain a matching guest tool, despite the separate native registration.
This narrows the failure to exposure between those layers; it does not identify
the exact cause or imply every configured stdio server is generally excluded.
No guest command call occurs. Private instructions and unrelated tool identifiers
are not published; selected model-authored code and benign lookup output are.

[Terminal record](results/solver-model-catalog-01/terminal.json): CLI0,10.124s,
outer90-second cap not reached. Input22,543 + output115 = **22,658 tokens**;
cached input11,008 is a subset of input, not additional tokens. These costs belong
to a diagnostic task, not a skill efficiency comparison. [Guest console](results/solver-model-catalog-01/guest.log)
observes readiness, zero responses and no graceful stop. The exact owned VM probe
is absent after CLI termination; this is not a graceful-shutdown claim.

No quality, savings, enforced host-tool isolation or native issue grading result.
No unchanged favorable retry. A prospective transport comparison can reuse the
HTTP MCP approach from `run_receipt_tool_bridge_01.py`, which reached original
model tool calls, with honest annotations and native readiness before any new
catalog observation. The earlier host-workspace approval rejection remains a
separate adverse result; guest transport does not authorize an approval bypass.
Ordinary skills, README onboarding, featured benchmark and live site unchanged.

한국어: 네이티브 등록은 됐지만 모델의 실제 ALL_TOOLS13개에서는 게스트 도구의
이름·고유 설명이 모두 검색되지 않았다. 원본 실행의 exec1회와22,658토큰을
보존한다. 서버 등록과 모델 노출 사이 문제로 범위를 좁혔으며, 구체 원인은
미확인이다. 과제 해결·절감 비교·강제 호스트 격리 증거가 아니며 같은 조건을
재실행하지 않는다. 다음 후보는 기존 실제 모델 호출이 있었던 HTTP MCP 방식이다.
