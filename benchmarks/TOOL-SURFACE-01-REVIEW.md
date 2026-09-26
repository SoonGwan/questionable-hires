# Tool-surface01: no configuration adoption — 2026-09-27

Measured execution sources **`e70238f6`**, CLI0.157.1, unchanged authored native
fix input. [Frozen protocol](TOOL-SURFACE-01-PROTOCOL.md),
[final three-session schedule](results/tool-surface-01/run.json),
[original cost/context/outcome review](results/tool-surface-01/review.json).
All three fresh serial Astra medium CLI turns completed without timeout, limits
or replacement. **Only default and apps_off completed the requested work.**
No skill was installed/invoked; `receipt` is case metadata only. This is an
availability probe, not an all-eight or skill efficiency measurement.

The official [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
documents per-invocation feature overrides. The [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents apps integration. Local CLI lists code_mode_host but that page does not
define it; the original execution below establishes this harness's constraint.
No persistent feature enable/disable, user configuration or account/key action.
Do not remove connectors/browser functionality from tasks that need it.

| Condition | First input tokens | Whole input+output | Responses | Seconds | Requested native outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| Default |14,057|44,133|3|20.242|Before2 tests/one real assertion failure; after2/2, exits1/0 |
| `--disable apps` |12,824|53,429|4|20.503|Same before/after observations, exact required one-line fix |
| `--disable code_mode_host` |14,073|42,764|3|13.507|No file read/edit or native test execution; unavailable tool |

Apps_off first input is8.77% smaller, but whole tokens21.06% higher and time1.29%
higher. The extra response remains included; it is not automatically unnecessary
work. These n=1 observations on one authored task, fixed order/shared host/cache,
and unobserved complete tool-schema/private-input differences do not establish
causal or representative gains. Recorded initial skill catalogs are empty in all
three; no catalog-only inference of executable availability. Native/initial-context
inspection is separate from an installed-skill body exposure claim.

Host_off emits the actual item error that Code Mode is unavailable and will fail
closed because its host is disabled. It attempts the same normalized `exec` tool,
but no direct-shell fallback or command execution occurs. The model explicitly
reports no tests/fix and unchanged files. Its smaller cost/time is **not saving**:
the required work did not occur. Do not adopt that setting. Apps_off does not
show whole-task efficiency, so no profile or global setting is adopted either.

Actual matching original session contexts verify Astra/medium in all three.
Existing per-response profiling reconciles CLI totals exactly; cached input is
included once within input, reasoning not added again. No billing estimate.
Raw full sessions and initial inventories remain local. Each exported cell keeps
selected original tool records/line hashes, CLI commands, output, answer and source
excerpts. Nested condition run.json files are preparation manifests; the root
schedule/cell metadata supply original completion, not task success.

Default/apps_off each execute the unchanged two native tests before/after using
actual app imports. The quantity assertion fails1≠2 before while the payload
control passes; both pass after. Final producer bytes match only return1→return2.
Tests, instructions, uncommitted owner note and other supplied bytes/modes remain
unchanged. Host_off has no producer change. All three captured initial versus
before-collector index bytes/modes match. These are scoped final observations,
not proof of every transient action/all Git metadata or other tool capability.

## Collector correction, separate from measured execution

The original collector's top-level error_event_types misses an error emitted as
`item.completed` with `item.type=error`. Host_off's completed CLI turn therefore
has usage and completed=true even though requested work is unavailable. That
completed field is CLI-turn completion, never a task success score.

Add **item_error_review_candidates** with item identity/message to capture
review diagnostics. Preserve original events, usage, command results and existing
completion logic. A warning can recover before valid native evidence, so the new
field is a review prompt rather than an automatic task failure. Historical model
metadata is unchanged; [post-timing replay of its original stream](results/tool-surface-01/author-controls/original-host-off-new-diagnostic.json)
now exposes the missed item error. This is not a new model execution or repaired
original task outcome. Collector changes were made only after all probe sessions
finished; they are not the measured e70238f6 code.

The new regression fails before with an empty candidate list, then passes after.
A second regression preserves later native observations after an item warning.
[Checkout36/36](results/tool-surface-01/author-controls/item-error-after.txt),
[Git-free36/36](results/tool-surface-01/author-controls/collector-git-free.txt).
The first diagnostic-test attempt used a wrong class path; a mistaken insertion
into an embedded fixture then caused its SyntaxError. Both author harness errors
are retained, restored and corrected; neither is a passing before reproduction.
The actual [failing-before assertion](results/tool-surface-01/author-controls/item-error-before.txt)
is distinct. Initial collector archive omits three retained evidence fixtures and
export.py (four missing-file errors); corrected complete copying passes36/36.
No author test launches a model.

Before model launch, wrapper/freeze/stop controls pass7/7 in checkout and a Git-free
copy, with synthetic version probing. Initial Popen mock/version-capture collision
and unused first preparation are retained; no model attempt was restarted. Author
native preflight executes two tests, actual defect failure and corrected pass.
These controls do not measure model efficiency or certify a hosted release.
No skills, featured charts, deployed site, dependencies or CI change. The broader
all-eight quality/token/time objective remains unmet.

한국어: tool-surface01(2026-09-27,실행 소스`e70238f6`,CLI0.157.1)의3회 검사에서
앱 연동 제외는 첫 입력8.77% 감소지만 전체 토큰21.06%, 시간1.29% 증가다.
코드 실행 호스트 제외는 도구가 막혀 수정·테스트를 전혀 수행하지 못했다.
작업 실패를 절감으로 계산하지 않고 두 설정 모두 채택하지 않는다. 스킬은 설치·호출하지
않았고8개 역할의 성능 검증이 아니다. 이후 수집기에 실행 항목 오류 진단을 추가해
완료된 CLI 응답 속의 도구 오류를 놓치지 않도록 했다. 실제 실패 전후 회귀 증거와
체크아웃·Git 없는 복사본36개 통과를 보존하며 경고를 자동 실패로 바꾸지 않는다.
전체 품질·토큰·시간 개선 목표는 여전히 미달이다.
