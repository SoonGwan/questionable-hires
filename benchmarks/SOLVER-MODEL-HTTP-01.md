# Solver model HTTP01 — 2026-09-27

Parent `ec78d371`. Two distinct original model tasks: HTTP catalog inspection,
then one guest command attempt after inclusion is observed. Both use `gpt-6-astra`
medium effort and retain prior scoped flags. No issue-solving, grading inputs,
ordinary skill changes, quality score or efficiency comparison.

## Actual catalog inclusion

[Catalog manifest](results/solver-model-http-catalog-01/launch.json) uses the same
metadata-only prompt as [stdio catalog01](SOLVER-MODEL-CATALOG-01.md), replacing
the MCP transport with the separately native-verified localhost HTTP candidate.
The model-visible lookup and feature flags are unchanged. The HTTP server starts
before CLI launch; the empty owned project and exclusive guest log are new.

[Original rollout](results/solver-model-http-catalog-01/result.json) records one
exec call and actual **catalog_count14**, with `mcp__qh_guest__guest_command` and
owned guest-description match true. Stdio recorded13 and no matches. This pair
supports HTTP inclusion in these actual calls; it does not explain the underlying
stdio routing failure or establish general transport behavior.

Input22,574 + output130 = **22,704 tokens**, cached input11,008 already included.
[Terminal](results/solver-model-http-catalog-01/terminal.json): CLI0, server−2 after
owned SIGINT,18.812s, guest readiness/stop, zero guest commands, exact probe absent
and port closed. [Complete console](results/solver-model-http-catalog-01/guest.log)
retains the native observations. Catalog inclusion is not command authorization.

## First command rejected before guest execution

[Command manifest](results/solver-model-http-command-01/launch.json) freezes one
call to the observed exact tool identifier with `/bin/busybox uname -s`, cwd
`/solver`, timeout5. The prompt forbids fallback/repeat calls. The tool still
truthfully declares that its general command interface can mutate/delete guest
files. Personal configuration and approval overrides are not changed.

[Actual original rollout](results/solver-model-http-command-01/result.json)
records one exec call attempting that guest tool, then isError true:

> MCP tool call requires approval, but approval policy is never

This is an execution-policy rejection, not an observed automatic reviewer
decision or an actual guest command failure. No base64 stdout or command exit
code is returned; the model reports that absence. [Complete console](results/solver-model-http-command-01/guest.log)
has readiness/stop and **zero guest responses**, corroborating that the command
did not reach the guest. No fallback or favorable retry replaces this cell.

Input22,483 + output154 = **22,637 tokens**, cached input11,008 already included.
[Terminal](results/solver-model-http-command-01/terminal.json): CLI0, server−2 after
owned SIGINT,18.900s, exact probe absent and port closed. CLI0 is a completed model
turn, not successful tool execution. Neither cell uses forced server cleanup.

The first gate, actual HTTP model catalog inclusion, is now supported. Actual
model guest command authorization remains unmet. Do not change mutating tool
annotations or approval configuration to bypass this recorded rejection. Inspect
the actual permission contract before further model work; do not repeat the same
blocked command. Native SDK success is not substituted for model authorization.
No host-tool exclusion, selected issue grading or all8 quality/lower whole-task
tokens/faster completion claim. README, featured data and hosted landing unchanged.

한국어: 동일한 목록 검사에서 HTTP는14개와 정확한 게스트 도구 이름·설명 일치를
반환했다. stdio의13개·일치 없음과 구분해 기록한다. 이후 최초 실제 명령 호출은
승인이 필요한데 정책이 never라는 이유로 거절됐다. 게스트 응답0개이며 OS나
종료코드는 관측되지 않았다. 두 실행의 토큰22,704·22,637과 실패를 보존하며,
승인 설정이나 사실과 다른 읽기 전용 표기로 우회하지 않는다. 목록 노출만
확인됐고 모델 실행 권한·품질·토큰·속도 목표는 아직 미달이다.
