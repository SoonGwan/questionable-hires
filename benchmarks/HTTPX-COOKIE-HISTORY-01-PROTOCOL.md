# Redirect-cookie history: optional-selector transfer — 2026-09-15

Freeze before calls. Original Necromancer `da20939`, candidate `62195d8`.
Identical entry; candidate adds a named-function selector/reference and a
conditional link from the focused-history guide. No requirement to use any helper.
New authored cookie ticket, but the same source and neighboring redirect/history
code as earlier experiments: this is **near transfer, not independent generalization**.
Source HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`, full local history.

## Exact shared task

Substitute the same existing interpreter for `<PREINSTALLED_PYTHON>`.

> Review removing only `headers.pop("Cookie", None)` from
> BaseClient._redirect_headers. Is that a behavior-preserving cleanup? Establish
> current necessity and locally evidenced history; do not implement the removal.
>
> Compare current and proposed behavior using actual Client/MockTransport requests
> with trust_env=False and follow_redirects=True. For each scenario use a fresh
> client, GET https://example.invalid/start, return a 302 at /start and a 200 at
> the destination. Seed client.cookies with sid=old, domain=example.invalid,
> path=/ except in case 5. Record both initial and redirected Cookie headers and
> request URLs in each version for these five cases:
> (1) Location /done, Set-Cookie: sid=new; Path=/;
> (2) Location /done, Set-Cookie: sid=gone; Path=/; Max-Age=0;
> (3) Location https://other.invalid/done, no Set-Cookie;
> (4) Location /done, no Set-Cookie;
> (5) initially empty jar, Location /done, Set-Cookie: sid=new; Path=/.
> Use these synthetic cookies only. Explain the mechanism and which cases change
> or remain equivalent. Do not infer browser behavior or remote server acceptance.
>
> Inspect relevant local history and an earlier operational implementation,
> including how it constructs redirected requests with cookies. Distinguish code
> movement/line attribution from behavioral introduction. Support earlier presence
> with actual ancestor code; first-ever origin/intent is not required and must not
> be invented. Use only ancestors of pinned HEAD, not other branch tips or external
> issue pages. Give a retain/simplify/remove recommendation with current and
> historical evidence and behavior to preserve.
>
> Preserve original project files and installed resources. No network, installs,
> fetching, commits or publishing. In-memory substitutions or owned disposable
> copies are permitted; no particular technique is required. Use
> <PREINSTALLED_PYTHON> with -B; pytest additionally with -p no:cacheprovider.
> Scratch must stay inside this project and be removed before finishing. Captured
> output is sufficient; no separate report/harness is required.

## Preflight and scoring

`preflight_httpx_cookie_history.py` / `httpx-cookie-history-01-preflight.json`:
native redirect-cookie test passes; ten two-request observations match explicit
expectations; a deliberate stale-versus-new assertion fails with actual values.
The author mutation removes exactly the one expression, with original compiler
flags/bindings intact. All 125 tracked source files stay unchanged, no bytecode.
An initial pre-freeze historical-text check incorrectly expected lowercase
`cookie`; it failed, was corrected to the observed `Cookie`, and rerun. No model
cell was launched against that author check, and behavioral inputs were unchanged.

Current redirected cookies: new, absent, absent, old, new. Proposed: old, old,
old, old, new. Initial headers: old in cases 1–4, absent in 5, both versions.
Earlier middleware before `00e150f` has both header removal and cookie-aware
request construction. Equivalent earlier evidence is valid. Score required
observations, mechanism, historical support and scope; helper use is recorded,
not rewarded. Source excerpts alone do not substitute for live observations.
Author preflight/answers are not model inputs.

## Execution

Two fresh serial GPT-6 Astra / medium persisted sessions, **original then
candidate**, one per condition, 360 seconds each. Snapshot every skill resource
at the exact revisions; identical model prompts. No no-skill arm. Store manifests
before execution. Preserve all failures/timeouts and both complete cost records;
no favorable retry or task modification. Stop on actual account limits.

Review original traces for guide/selector adoption and output completeness before
interpreting total input (including cached) + output tokens and elapsed time.
No automatic efficiency win for incomplete/unequal work. Shared host/cache, n=1,
near-transfer source and fixed order limit inference. Keep previous adverse
results; no featured/chart promotion from this pair.

한국어: 같은 HTTPX 저장소의 인접 코드를 쓰는 새 쿠키 과제로, 일반화 검증이 아닌
근접 전이 비교다. 도구를 강제하지 않고 이전·현재 스킬의 실제 사용과 전체 비용을
살핀다. 원본/수정 동작 각 5개, 실패·대조 사례와 이력을 먼저 고정했다. 좋은 결과만
재시도하거나 그래프로 승격하지 않는다.
