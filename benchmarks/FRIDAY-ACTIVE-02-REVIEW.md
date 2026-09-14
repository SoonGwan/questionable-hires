# Friday discovery 02: fewer reads, broad gain unproven — 2026-09-15 KST

Launch `8e66077eb08b2cd0ee3fe81f3551f5e289fb2f51`, resources `636935e`.
[Protocol](FRIDAY-ACTIVE-02-PROTOCOL.md),
[both original-session exports](results/friday-active-02/summary.json).
Two scheduled skill sessions completed without timeout, limit stop or retry.
Previously exposed synthetic tasks, one repeat, no fresh baseline. Historical
comparisons below are development feedback, not causal or held-out estimates.

| Case | Prior skill tokens | Candidate tokens | Prior seconds | Candidate seconds | Shell calls |
| --- | ---: | ---: | ---: | ---: | --- |
| A | 91,524 | 71,659 | 62.782 | 57.818 | 6 → 3 |
| B | 71,466 | 71,534 | 64.359 | 58.138 | 4 → 3 |
| Sum | 162,990 | 143,193 | 127.141 | 115.956 | 10 → 6 |

Compared with active-01's skill, summed tokens fall 12.15% and time 8.80%.
**B tokens increase by 68**, despite one fewer command. Compared with the
historical no-skill baseline, candidate sums remain **6.37% more tokens and
1.73% more time**. Input includes cache; output is added once. Neither comparison
has fresh paired controls, and diagnostic work differs. No general savings claim.

## Observable adoption and evidence

Both sessions perform one hidden-file inventory with the correct `!.git` glob,
then read entry/release/requirements/SQL/readers/notes together, then run native
SQLite. Git objects no longer appear in their inventories. A also checks the
possible applicable AGENTS.md paths in that grouped command. B's complete visible
inventory contains no AGENTS.md. No supplied instruction file was skipped here;
this does not establish handling of ignored or external ancestor instructions.
The correct initial inventory happens before entry reading, so its improvement
cannot be causally attributed to a paragraph the model has not yet read. Grouped
reads also include the entry itself. This screen shows a compatible behavior
change, not proof of when/how the new instruction influenced it.

Neither session loads the optional matrix guide or script. Both use actual
supplied SQL and AST-extracted literal queries on one in-memory database, observe
all five checkpoints, compare exact columns and rows, and retain inactive-reader
diagnostics. A collects contract failures and asserts none; B records the first
active mismatch/error while continuing diagnostically to recovery. B's outer exit
0 is not release approval: its original output contains the rollback-start
missing-column failure and its answer blocks the plan. Both leave production
application writers, locking, orchestration and staging unverified.

A adds table-info queries and a final row assertion compared with prior skill A.
B adds table-info queries while preserving direct stored-row observations.
All supplied post-write values and identities survive rollback in the actual
captures. These are full original observations, not filled by author replays;
no independent counterfactual witness replay was performed in this screen.

## Integrity and decision

Raw turn usage reconciles with metadata, raw CLI streams with stored/redacted
events, and public events/source hashes with the originals. Frozen case hash
matches the manifest. Installed resource before/after inventories agree and
their bytes/modes match the candidate. All eight supplied files and full exported
project file sets match frozen inputs; no retained scratch or edits. All six
commands exit 0 with actual output. Export scan finds no home/temp paths or
key-shaped strings. Original captures remain unchanged.

Keep this small candidate provisionally: desired grouped reads are observed and
scoped SQL evidence remains intact. Do not add more discovery instructions or
force matrix use. Stop iterating this same pair for better-looking numbers; next
behavioral evidence should transfer to a different layout/domain with relevant
project instructions and nontrivial reader discovery. A fresh comparison remains
necessary to judge net model efficiency. Historical/featured charts stay frozen.

## 한국어

새 두 세션 모두 명령 3번으로 입력을 묶어 읽고 실제 SQL 검증까지 끝냈다.
이전 스킬의 6번·4번보다 줄었고, 정상 배포와 중간 롤백 오류·최종 데이터 복구를
구분하는 근거도 유지됐다. 다만 첫 파일 탐색은 스킬 본문을 읽기 전이므로,
올바른 제외 패턴이 새 문단 때문에 생겼다고 단정할 수 없다.

이전 스킬 대비 합산 토큰 12.15%·시간 8.80% 감소가 관측됐지만, 오류 과제의
토큰은 68개 늘었다. 과거 스킬 없는 기준보다도 토큰 6.37%·시간 1.73%가 높다.
신규 기준군이 없고 동일 과제를 재사용했으므로 일반 성능 향상은 미입증이다.

원본·공개용 결과·입력 파일·리소스를 대조했다. 도우미 채택은 없었다. 현재 후보를
잠정 유지하되 같은 과제에서 유리한 수치를 반복 추구하지 않고, 다른 프로젝트
구조에서 지침 탐색과 실제 검증이 함께 유지되는지 확인할 필요가 있다.
