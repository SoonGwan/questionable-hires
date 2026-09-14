# History guide disclosure — 2026-09-15

Launch `9ccd466`; original `28caeb8`, candidate `3a04643`.
[Frozen protocol](../../HISTORY-GUIDE-01-PROTOCOL.md), [arithmetic](comparison.json),
[preflight](preflight.json). Same exposed real HTTPX ticket and full-history source
`26d48e0634e6ee9cdc0533996db289ce4b430177`; not a new held-out task.
Two fresh persisted Astra medium sessions, original then candidate, n=1 each,
serial, 360-second limits. Both completed; no timeouts, account limits or retries.

| Observation | Original | Candidate |
| --- | ---: | ---: |
| Input + output tokens, cached input counted once | 195,535 | 264,384 |
| Process wall time | 114.804s | 124.058s |
| Shell commands / outer calls | 10 / 5 | 8 / 7 |
| Changed history guide read | No | No |
| Details read / collector executed | No / No | No / No |

**No demonstrated improvement:** +35.21% tokens, +8.06% time. Neither reads any
changed reference, so this is not an attributable effect of the guide split.
Identical entries were present in both recorded initial contexts before tools;
catalog mentions do not establish executable availability or disable enforcement.
Fewer shell commands did not mean fewer outer calls or less total work.

Both retain the fallback, show all ten required actual Client/MockTransport
observations, distinguish omitted request auth from explicit None, and establish
earlier URL-auth behavior from ancestor client and middleware code. Cases 1 and 4
lose URL-derived headers under the proposal; cases 2, 3 and 5 are unchanged.
Neither claims server acceptance or first-ever origin. Probe methods are restored
and all 125 original project files and installed resources remain byte-identical;
inventory has no extra non-skill/non-Git files.

Both initially fail a formatting-sensitive `ast.unparse` comparison before the
actual header probe. Original repairs it with structural target checks; candidate
compares parsed AST structure. These setup failures are not application defects
and their costs remain. Candidate's failed probe shares a shell command with later
successful Git commands: its final shell status is zero, **not proof every step
passed**. Original also has a no-match discovery command returning 1.

Capture: 8/10 original and 6/8 candidate shell output/exit pairs exactly match
stored original responses after normalization. Other reads include explicit
truncation or truncated outer captures; do not reconstruct them as model-visible
evidence. Both complete ten-header outputs match exactly, and later targeted
ancestor reads supply the historical evidence. No missing/unmatched/duplicate
outer tool IDs. Full private rollouts stay local; selected records only are exported.

- Original: [answer](original/auth-history--skill--1/answer.md),
  [commands](original/auth-history--skill--1/commands.json),
  [original tool records](original/auth-history--skill--1/tool-records.json),
  [initial context check](original/auth-history--skill--1/initial-context.json).
- Candidate: [answer](candidate/auth-history--skill--1/answer.md),
  [commands](candidate/auth-history--skill--1/commands.json),
  [original tool records](candidate/auth-history--skill--1/tool-records.json),
  [initial context check](candidate/auth-history--skill--1/initial-context.json).

Decision: retain the smaller optional interface as organization, not a measured
performance improvement. Do not force adoption or rerun this ticket to obtain a
favorable score. Future work needs a decision-changing bottleneck beyond this
unread reference. No chart promotion. Fixed order, shared host/cache, n=1 and reused
task preclude causal or broad eight-skill claims.

한국어: 수정본은 토큰 35.21%·시간 8.06% 증가했다. 양쪽 모두 바꾼 안내를 읽지
않아 안내 분리의 효과로 해석할 수 없다. 필요한 열 번의 관측과 이력 판단은
확인했지만, 초기 탐침 실패와 일부 잘린 기록도 그대로 보존한다. 문서 정리는
유지하되 성능 개선으로 홍보하거나 같은 과제를 유리할 때까지 재실행하지 않는다.
