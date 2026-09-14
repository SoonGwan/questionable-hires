# SQLite debit — 2026-09-15 development screen

Launch `eb6f41a`; Con Artist original `6eef303`, candidate `ed4a38a`.
Both explicit skill, GPT-6 Astra / medium, one fresh persisted session each,
serial original then candidate, 240-second limit. This is an authored synthetic
task, not an independent project holdout. See the
[frozen protocol](../../SQLITE-DEBIT-01-PROTOCOL.md) and [comparison](comparison.json).

| Observation | Original | Candidate |
| --- | ---: | ---: |
| Total input + output tokens (cache included once) | 141,497 | 137,419 |
| Process wall time | 91.698s | 84.771s |
| Shell commands / outer tool calls | 9 / 6 | 11 / 6 |
| Required audit and test improvement | Complete | Complete |
| New helper adopted | No | No |

Recorded differences are **−2.88% tokens / −7.55% time**, not evidence that the
new replacement API improved performance. Neither reads its references nor
executes a skill helper. Shared host/cache, fixed order and n=1 are confounds;
original also overlapped a 1.136-second local seven-test helper check. Candidate
ran each correct/faulty pair in parallel; original ran them serially. No retries,
chart promotion or broad 20–30% claim.

## Reviewed original evidence

Both inspect the actual transaction and fixtures, replace only commit with
rollback in disposable copies, and preserve the successful acknowledgment.
Original cases pass on both correct/faulty implementations; improved cases pass
correct code and fail faulty code on `balances["alice"] == 100 - amount`:
actual 100 versus expected 93/87. Bob remains 250. Both retain acknowledgment and
both fixture amounts, read from a newly opened connection and explicitly close it.
Both also run the final improved original project: two passes.

Each writes its own pytest hook for copied binding and post-call balances.
Original uses a root conftest hook; candidate uses `-p audit_probe -s`.
Both hooks exercise real fixtures and SQLite, not a simulated implementation.
Original's first setup search and candidate's last instructions search exit 1
for no matching configuration/instruction files; these are not test failures.

All **20 shell outputs/exits** exactly match corresponding original stored tool
responses after path/newline normalization, including all five native outcomes
per arm. No missing, unmatched or duplicate outer call/output IDs. Selected
redacted tool records are included; full rollouts stay local because they contain
private instructions. Source hashes refer to unredacted originals. This review
uses original execution, not an author rerun.

Only `tests/test_debit.py` changes in each actual workspace; production, native
fixtures, README and installed skill resources remain unchanged. File inventories
contain only the four supplied project files outside Git/skills. Models remove
their audit scratch and fixture databases. The resulting tests are behaviorally
identical apart from import ordering. Limits include crash durability,
concurrency and distinct wrong-account faults, which were not tested.

`<PREINSTALLED_PYTHON>` replaces the same local preinstalled Python path in exports;
Python 3.9.6 / pytest 8.3.4. Exact fixture/task and resource digests were frozen
before launch. Author preflight is separate and excluded from model inputs.

한국어: 두 스킬 모두 실제 SQLite 결함을 확인하고 같은 의미의 테스트를 보강했다.
기록상 토큰 2.88%, 시간 7.55% 감소지만 새 도우미를 둘 다 사용하지 않아 개선
효과로 귀속할 수 없다. 합성 과제 각 1회·고정 순서·공유 환경이며 일부 로컬
검사도 겹쳤다. 원본 응답과 명령 출력 20개를 대조했고, 다섯 번의 실제 검사와
원본 보존·정리를 확인했다. 대표 그래프와 전체 성능 주장은 변경하지 않는다.
