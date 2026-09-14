# URL-auth history: original versus candidate — 2026-09-15

Launch `46906bf`; [frozen protocol](../../HTTPX-AUTH-HISTORY-01-PROTOCOL.md).
Original skill `488515f`, candidate `f1c30e3`; only the 224-byte compiler-context
addition in `SKILL.md` differs. Both use the same full HTTPX source
`26d48e0634e6ee9cdc0533996db289ce4b430177`, 125 files, 1,499 ancestor commits.
Two fresh serial Astra medium sessions, candidate then original, one each,
360-second limits. This is **not** a no-skill comparison.

## Result: mechanism adopted, overall cost mixed

| Measure | Original skill | Candidate |
| --- | ---: | ---: |
| Total input + output tokens, cache included | 222,756 | 231,925 |
| Process wall time | 114.915s | 103.034s |
| Compiler setup failures | 1 | 0 |
| All failed shell commands | 2 | 1 |
| Shell commands | 9 | 8 |
| Outer tool calls | 6 | 6 |

Candidate records **4.12% more tokens / 10.34% less time**. Both correctly reject
the proposed compatibility removal, show all ten required current/proposed
headers and explain current precedence and earlier live URL-auth behavior.
No required case is omitted to reduce cost. Keep the candidate as narrowly
supported probe-context guidance, **not as an accepted net efficiency win**.
One pair and differing extra work cannot establish a causal or general gain.

Candidate reads the actual module AST, preserves its `__future__` imports, retains
the method's globals, and compiles with `dont_inherit=True`. It removes exactly
the specified assignment/guard and executes all ten observations in one probe.
Original extracts method text without that context and fails before any Client
observations (`TypeError` evaluating a union annotation under Python 3.9). It
adds postponed annotations and runs the ten observations successfully. Original
failure and repair cost are retained; no author retry changes either outcome.

## Actual observations and work

The successful probes agree on all cases. Names below identify only the explicitly
synthetic credentials from the ticket; exact emitted Basic header values remain
in the original outputs.

| Case | Current | Proposed |
| --- | --- | --- |
| URL only | URL-derived auth | absent |
| Client overrides URL | client auth | client auth |
| Request overrides client | request auth | request auth |
| Explicit None with URL/client | URL-derived auth | absent |
| Explicit None without URL | absent | absent |

Both distinguish omitted request auth (use client selection) from explicit None
(bypass client selection, but URL fallback still applies). Both prove prior
operational fallback in parent `206c5372` of the 2019 client-auth movement commit,
including middleware selection and header construction. Both avoid treating
that older caller's `None` semantics as identical to today's. Neither claims
first-ever origin or remote server acceptance.

Both read the optional history guide but do not invoke its collector. Candidate
examines an additional auth-normalization commit and prints broad historical
diffs; original uses different diff context and targeted follow-up windows. Both
also search a nonexistent `tests/test_auth.py` within larger commands and have a
final instruction-file search return 1 because no matching file exists. These
costs remain; they are not application defects or missing required evidence.
Avoided compilation alone does not explain overall resource cost, and guide
reading is not adoption of the compact/multi-range collector.

## Original evidence and limits

| Evidence | Original | Candidate |
| --- | --- | --- |
| Answer | [answer](original/auth-history--skill--1/answer.md) | [answer](candidate/auth-history--skill--1/answer.md) |
| CLI commands | [commands](original/auth-history--skill--1/commands.json) | [commands](candidate/auth-history--skill--1/commands.json) |
| Stored tool responses | [records](original/auth-history--skill--1/tool-records.json) | [records](candidate/auth-history--skill--1/tool-records.json) |
| Author integrity | [integrity](original/auth-history--skill--1/author-integrity.json) | [integrity](candidate/auth-history--skill--1/author-integrity.json) |

Twelve of seventeen command outputs/exit codes match stored responses exactly.
Four historical/source responses have explicit middle truncation. One candidate
outer output is also explicitly truncated, leaving its JSON block unparseable;
the fuller CLI output is not reconstructed as model-visible evidence. Targeted
original reads retain required current/historical evidence and both complete
ten-observation outputs match exactly. Original parallel results require unwrapping
two indexed `{i, result}` records. No missing/unmatched/duplicate selected tool
call IDs. Full rollouts remain local; selected reviewed records and source hashes
are exported. CLI command text masks some public `password` expressions; stored
original tool calls retain the public source-removal expression, with synthetic
credentials only. No private credentials are used or recovered.

All 125 original source files per arm remain byte-identical, installed resource
manifests unchanged, no extra project files or bytecode retained. Reviewed commands
show no source edits, fetching/network, installs, commits or delegation. Final
identity alone cannot prove no transient mutation. Six selected source/license
files are exported, not the full repository/history. Paths are normalized; source
hashes refer to unredacted originals. [Arithmetic](comparison.json),
[schedule and ticket](run.json).

This confirms an observed use of the intended setup safeguard, not lower total
tokens or broad skill superiority. Shared host/cache, candidate-first order and
n=1 remain limitations. Do not relabel the earlier redirect pair's 31.80% token
reduction as a result of this new instruction. Featured charts remain unchanged.

## 한국어

수정 전·후 스킬을 새 URL 인증 과제로 직접 비교했다. 두 조건 모두 필수 10개
관찰과 역사적 근거를 충족했다. 수정본은 원래 컴파일 설정을 보존해 준비 오류
없이 실행했고, 이전 스킬은 한 번 실패한 뒤 고쳤다. 하지만 수정본은 전체 토큰
4.12% 증가·시간 10.34% 감소로 혼합된 결과다. 오류 방지 안내로는 근거가 생겼지만
전체 효율 개선으로 채택하지 않는다. 추가 이력 조회·탐색 실패·잘린 출력도 공개하며,
이전 31.80% 절감 결과를 새 안내의 성과로 바꾸거나 그래프를 승격하지 않는다.
