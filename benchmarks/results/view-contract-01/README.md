# SQL view contract — 2026-09-15 development screen

Launch `e1324fc`. Friday original `c5eddbc`, candidate `45a2741`; identical entry,
candidate adds an optional native row-assertion API and mode documentation.
[Frozen protocol](../../VIEW-CONTRACT-01-PROTOCOL.md),
[comparison](comparison.json), [author preflight](../../view-contract-01-preflight.json).

This is a targeted **authored synthetic** SQL-only task, not a real-project
holdout. Two fresh persisted GPT-6 Astra / medium sessions, original then candidate,
one each, serial cells, 240-second cap; no retries or concurrent author test runs.

| Observation | Original | Candidate |
| --- | ---: | ---: |
| Total input + output tokens, cache included once | 73,855 | 74,355 |
| Whole-process time | 65.886s | 77.144s |
| Shell commands / outer tool calls | 3 / 3 | 3 / 3 |
| Required checkpoints / reader observations | 5 / 10 | 5 / 10 |
| Matrix, new assertion API or guide used | No | No |

**No measured improvement:** candidate records +0.68% tokens / +17.09% time.
Neither reads changed resources, so these numbers do not establish an API
regression either. Fixed order, shared host/cache, targeted synthetic task and
n=1 limit interpretation. No favorable retry, chart promotion or all-eight claim.

## Original evidence

Both read all supplied inputs, extract literal queries without importing the
reader module and execute the actual four SQL files in one in-memory sequence.
Both queries run at all five checkpoints, including the unchanged-schema restart.
Full ordered tuples, column labels and actual Python BLOB bytes are checked.
The executed SQLite engine reports 3.51.0 in both cells; author preflight is
separate, not the model execution record.

Both identify phase 2 as the first blocker: OLD's SELECT succeeds, but returns
`title` where its exact column contract requires `label`. OLD remains incompatible
through phases 3/4. NEW's errors in phases 1/5 are inactive observations, not
active blockers. Phase 5 restores OLD and preserves the updated, unchanged and
new rows, including all BLOB bytes. Both explain that restarting OLD before down
is insufficient. Both recommend a coordinated non-overlapping cutover if supplied
contracts must remain fixed, or versioned views/reader changes if coexistence is
required; neither implements that strategy change.

Supplementary work differs: original explicitly queries SQLite payload storage
types; candidate adds a final integrity check. Both query underlying table data
at every checkpoint. These are not identical optional checks, but required
contract observations and scoped conclusions are complete in both.

All **six shell output/exit pairs** exactly match original stored tool responses
after path/newline normalization. No missing, unmatched or duplicate outer call/
output IDs. All six supplied files and installed resources remain unchanged;
actual workspace inventories contain no extra files outside Git/skills. Neither
creates scratch or changes production. Selected redacted tool records are included;
full private rollouts stay local and source hashes identify unredacted originals.
These findings use original execution, not an author replay.

## Follow-up, not measured by this pair

Both first list files, then read the already-supplied release note with discovered
inputs, then execute. Make the native-path entry more explicit about combining
necessary discovery with already-known release inputs, without forcing a helper,
skipping instructions, reducing checks or collecting unrelated files. This is an
unmeasured entry clarification, not a retroactive gain for these cells. Do not
add another helper or force adoption to make this fixture favor the candidate.

한국어: 두 버전 모두 다섯 단계·열 번의 실제 SQL 관측과 정확한 판정을 완료했다.
수정본 기록은 토큰 0.68%, 시간 17.09% 증가였다. 새 API와 문서를 둘 다 읽지
않았으므로 API의 향상이나 악화로 귀속하지 않는다. 원본 응답 여섯 개와 파일
보존을 확인했고 불리한 결과도 보존한다. 후속 수정은 첫 목록 조회와 이미 알려진
릴리스 문서 읽기를 묶는 안내다. 해당 안내의 효과는 아직 미측정이며 그래프는 유지한다.
