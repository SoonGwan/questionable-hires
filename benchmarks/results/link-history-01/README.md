# Link-parser transfer — 2026-09-15

Launch `f76ee9c`; original Necromancer `37f827c`, candidate `24840f0`.
[Frozen protocol](../../LINK-HISTORY-01-PROTOCOL.md), [comparison](comparison.json),
[author preflight](preflight.json). A new authored ticket on the same pinned real
HTTPX source, deliberately selected for Python substitutions: near transfer,
not independent generalization or a no-skill comparison.

Two fresh persisted Astra medium sessions, original then candidate, serial,
n=1 each, 360-second limits. Both completed without timeout or account limit.
No retries or concurrent author test runs.

| Observation | Original | Candidate |
| --- | ---: | ---: |
| Total input + output tokens, cached input counted once | 115,744 | 130,443 |
| Process wall time | 85.241s | 90.783s |
| Shell commands / outer calls | 5 / 4 | 7 / 5 |
| Probe setup failures | 0 | 0 |
| Complete required mappings | 18 / 18 | 18 / 18 |
| Additional existing tests | 6 passed | 6 passed |
| Structural AST matching used | No | No |

**No demonstrated performance gain:** candidate +12.70% tokens / +6.50% time.
Both parse source/compiler context, but select the requested change by an exact
original-source substring with a one-match guard, not by comparing AST structure
or unparsed formatting. This is a valid technique: the new conditional guidance
was not exercised, and neither suffered the failure it addresses. Do not attribute
the resource difference to that mechanism or require AST adoption to obtain a win.

## Actual work

Both produce all 18 complete mappings through the actual `Response.links` public
property, with independently substituted A/B parsers and restoration in `finally`.
The captured mappings exactly match the frozen expected current/A/B observations:
A changes cases 4–6, B only case 5; no observation raises an error. Both explain
the caught unpacking failures, parameter-loop break and public `rel`/URL mapping
keys, rejecting both proposals as compatibility-preserving cleanup while allowing
B could be considered a separately authorized behavior change.

Both inspect relocation `41597adf` and actual earlier parser/caller at its parent
`6212e8fa`, distinguishing movement/renaming from introduction. Neither invents
first-ever origin or intent. They additionally run the same six existing parser
tests successfully (21 other tests deselected, not failures or full-suite passes).
All 125 project files and installed resources remain unchanged; inventories contain
no added non-Git/non-skill files or scratch.

Candidate has an extra discovery call and separates the existing test run from
final history/status checks. Original has one no-match instruction discovery exit
1; this is not a failed behavioral probe. These observed differences and shared
host/cache limit interpretation of the totals.

## Original evidence

All **12 shell output/exit pairs** exactly match stored original responses after
path/newline normalization; no command output is marked truncated. Both entries
are present in recorded initial context before the first tool. No missing,
unmatched or duplicate outer tool IDs. Catalog presence is not proof of executable
availability or requested disable enforcement. Full private rollouts remain local.

- Original: [answer](original/link-history--skill--1/answer.md),
  [commands](original/link-history--skill--1/commands.json),
  [stored tool records](original/link-history--skill--1/tool-records.json),
  [initial-context check](original/link-history--skill--1/initial-context.json).
- Candidate: [answer](candidate/link-history--skill--1/answer.md),
  [commands](candidate/link-history--skill--1/commands.json),
  [stored tool records](candidate/link-history--skill--1/tool-records.json),
  [initial-context check](candidate/link-history--skill--1/initial-context.json).

Decision: preserve the adverse observation and locally verified conditional
guidance, without claiming a speedup. Do not tune or rerun this ticket to reach
a target percentage. More single-case wording changes here lack a demonstrated
whole-task benefit; move beyond this HTTPX history-task family. Featured graphs
and all-eight performance claims remain unchanged.

한국어: 필수 결과 18개와 이력 검토는 양쪽 모두 정확했지만 수정본은 토큰
12.70%·시간 6.50% 증가했다. 둘 다 원본 문자열 치환으로 한 번에 실행해 새 AST
비교 안내를 사용하지 않았다. 원본 응답 12개를 모두 대조했고 파일도 보존됐다.
이 과제를 반복해 목표 수치를 맞추거나 단일 결과를 전체 개선으로 홍보하지 않는다.
