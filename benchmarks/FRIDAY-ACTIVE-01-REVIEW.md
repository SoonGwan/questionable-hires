# Friday active consumers 01: correct, more expensive — 2026-09-15 KST

Launch `fc577c904cfb051361435e7949fe1d0bc8662391`, resources `8153fec`.
[Frozen protocol](FRIDAY-ACTIVE-01-PROTOCOL.md),
[all four exported sessions](results/friday-active-01/summary.json).
All four scheduled sessions completed without timeout, account-limit stop or retry.
These two correlated synthetic variants have one observation per arm, not a
production sample or a broad estimate about the eight skills.

| Case | Baseline tokens | Friday tokens | Baseline seconds | Friday seconds |
| --- | ---: | ---: | ---: | ---: |
| A: compatible ordering | 66,977 | 91,524 | 55.115 | 62.782 |
| B: premature old reader | 67,638 | 71,466 | 58.864 | 64.359 |
| Sum | 134,615 | 162,990 | 113.979 | 127.141 |

Tokens are input including cache plus output, without double-counting cached or
reasoning tokens. Observed sums increase **21.08% tokens and 11.55% elapsed time**.
Both pairs regress on both metrics. Work differs, so these are descriptive costs,
not a causal estimate of instruction overhead. No chart promotion or hidden rerun.

## Actual behavior

All four execute the actual SQL and extract the supplied literal QUERY constants
with Python AST. They keep one in-memory database through five checkpoints and
observe exact columns and initial/post-write rows. Both A answers correctly find
local compatibility. Both B answers identify the active old reader's missing
`name` at rollback starts; they continue diagnostically to down.sql and observe
preserved updated, untouched and inserted records. They distinguish this final
recovery from a compatible sequence and explicitly leave production unknown.

Native output, not answer tables alone, contains the successful active columns
and complete rows, and B's actual missing-column error. B baseline prints reader
comparison booleans plus asserted stored rows; B skill uses row/column assertions
inside a caught failure collection. Their outer Python exit 0 does not mean the
release is safe: both retain and report the active failure. No later author replay
is used to fill original evidence. This review does not independently mutate every
retained witness or prove a general-purpose harness.

Every session also probes inactive readers and distinguishes those failures from
active blockers. Neither Friday session reads the optional matrix guide/script:
the new phase-selection implementation is **not adopted or measured** here.
Native SQL is an allowed route. Do not force helper use simply to market a feature.

Baseline A adds table-info observations at each phase; baseline B adds those and
stored-row checks. Friday B also adds direct stored-row checks. Friday A uses six
shell calls versus baseline A's three; Friday B uses four versus baseline B's
three. The skill traces include repeated file discovery, separate source reads
and hidden inventories listing Git objects because their exclusion glob contains
an extra space. They never read the matrix implementation. Extra discovery is an
observed optimization candidate, not proof that another paragraph will save 20%.

## Integrity and audit limitation

Original turn-completion usage matches metadata. Frozen cases match the manifest
hash; both installed resource inventories are unchanged and match the recorded
Friday resource digest. All eight supplied file contents and the entire exported
project file set match the frozen cases for all four cells; no retained scratch
or implementation edits. Export source hashes match raw artifacts and event text
matches path-redacted original stored events. Public artifacts retain all commands
and answers. A scan for local home/temp paths and key-shaped strings found no hits.

The first author integrity command stopped on an overly strict assertion that
every shell command had status `completed`. Baseline A item_2 has status `failed`,
exit 1: its source-file reads succeeded, then a trailing `rg` for AGENTS.md had no
matches. Its later SQL command succeeded and contains the full observations.
The follow-up audit explicitly retained/checked that one nonzero command rather
than relabeling it or rerunning the model. All four source/export reconciliations
then passed. No raw evidence was modified.

Decision: retain the optional helper capability but do not claim measured adoption
or efficiency. Address redundant discovery with a narrowly scoped candidate;
preserve current-consumer, transition and rollback evidence. Review a fresh
comparison before claiming that a read-budget change improves whole-task cost.

## 한국어

두 과제 모두 기준·스킬이 정상 순서와 실제 롤백 오류를 정확하게 구분했다.
하지만 스킬 합산 비용은 **토큰 21.08%, 시간 11.55% 증가**했다. 두 과제 모두
증가했고, 이 결과를 숨기거나 새 도우미의 성과로 표현하지 않는다.

스킬은 새 도우미를 읽거나 사용하지 않았고 직접 SQLite를 실행했다. 비활성
조회도 추가 검사했으며, 반복 파일 탐색과 분리된 읽기가 관측됐다. 정상 과제의
명령 수는 기준 3번·스킬 6번이었다. 다음 개선 후보는 이 중복 탐색이지만,
아직 비용 증가의 인과관계나 수정 후 절감률이 입증된 것은 아니다.

원본 사용량·리소스·8개 입력 파일·공개용 결과를 모두 대조했다. 기준 A의 파일
읽기 후 검색에서 나온 종료 1은 SQL 실패와 구분해 그대로 보존했다. 현재 성능
그래프는 변경하지 않는다. 기존 모델 실행의 근거를 사후 재실행으로 채우지 않았다.
