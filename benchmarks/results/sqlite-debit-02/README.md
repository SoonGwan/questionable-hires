# SQLite debit: entry routing follow-up — 2026-09-15

Launch `2a176bc`; original Con Artist `ed4a38a`, candidate `87adf2a`.
Only the skill entry differs. Exact project/task reuse screen 01; this is a
**development intervention on an exposed synthetic fixture, not a holdout**.
[Frozen protocol](../../SQLITE-DEBIT-02-PROTOCOL.md),
[machine-readable comparison](comparison.json),
[prior screen](../sqlite-debit-01/README.md).

Two fresh persisted GPT-6 Astra / medium sessions, **candidate then original**,
one each, serial cells, 240-second cap, same preinstalled Python 3.9.6 / pytest
8.3.4. No retries or concurrent author test runs. Shared host/cache still applies.

| Observation | Original | Candidate |
| --- | ---: | ---: |
| Total input + output tokens, cache included once | 118,600 | 99,815 |
| Process wall time | 86.613s | 73.252s |
| Shell commands / outer tool calls | 7 / 5 | 6 / 4 |
| Required four phases and delivered improvement | Complete | Complete |
| Helper adoption / helper reference reads | No / No | No / No |

Recorded differences: **−15.84% tokens / −15.43% time**. Candidate combines
copying, four native executions, integrity checks, applying the improved file and
scratch cleanup into one shell operation. Original separates preparation,
execution and application/cleanup. Both batch their four test runs serially.
The result is consistent with fewer orchestration round trips, but does **not**
establish that the entry change caused the savings or that helper use was cheaper.

The unchanged `ed4a38a` resource recorded **137,419 tokens / 84.771s** as candidate
in screen 01, versus **118,600 / 86.613s** here as original. This visible run-to-run
variation cautions against attributing this single favorable pair to wording.
Do not pool screen 01's different original resource or label these independent
holdout repetitions. No chart promotion, broad 20–30% claim or omitted adverse data.

## Original execution review

Both trace the real SQLite update/commit/acknowledgment and native seeded/amount
fixtures. The deliberate fault changes only commit to rollback in disposable
copies. Original cases pass correct/faulty code, improved cases pass correct code
and fail the rollback with `balances["alice"] == 100 - amount`: actual 100 versus
93 and 87. Both keep Bob's 250 assertion, acknowledgment and both native amount
cases. New reader connections are explicitly closed. Both also run the final
original-project test and record two passes.

Final test files are **byte-identical**, SHA-256
`9a4145d043dbb36b1f2b96a2b61db8d50efd9b2bc7b8a001bd954bbc191fb1cf`.
Only that file changes. Original production, README, fixtures and installed
resource bytes remain unchanged; inventories contain only the four project
files outside Git/skills. Both remove audit scratch and fixture databases.

Supplementary instrumentation differs, not required acceptance work: original's
runtime hook checks implementation and fixture function paths and prints balances
after each call; candidate's collection hook checks copied implementation/test
paths and imported function identity. Candidate still executes the unchanged
native fixtures in every phase, and its actual improved assertions establish
fault-specific persisted values. No mocks or alternative implementation replace
the SQLite effect. Neither establishes crash durability or excluded cases.

All **13 shell output/exit pairs** match their original stored tool responses
after path/newline normalization, including all five native outcomes per arm.
There are no missing, unmatched or duplicate outer call/output IDs. Original
stored output and reviewed source, not an author replay, support these findings.
Redacted selected tool records are included; full private rollouts remain local.
Hashes identify unredacted originals; `<PREINSTALLED_PYTHON>` masks the same
supplied local interpreter path.

## Decision

Retain the optional route, without claiming its performance effect is proven.
The native path is valid and no helper use should be forced. Per preregistration,
stop tuning this fixture for adoption and move to another material bottleneck.
Do not add stronger universal execution rules from this single observation.

한국어: 이미 노출된 같은 과제로 안내 문구만 비교했다. 수정본은 같은 최종 테스트를
만들고 필요한 검사·원본 보존·정리를 마치면서 도구 왕복이 5→4회로 줄었다.
기록상 토큰 15.84%, 시간 15.43% 감소지만 도우미는 쓰지 않았고, 같은 이전 버전의
다른 실행에서도 큰 토큰 변동이 있었다. 따라서 안내 수정의 인과 효과나 일반적인
성능 향상을 주장하지 않는다. 원본 응답 13개를 대조했고, 대표 그래프는 유지한다.
이 과제에서 도구 채택을 유도하는 추가 튜닝은 중단하고 다른 실질적 병목으로 이동한다.
