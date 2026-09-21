# Cachetools audit01 — mixed whole-task cost, changed helper unused

2026-09-21. Frozen launch `011f8b9`; prior resource `51a4f5a`, current
`b1875a0`. [Protocol](CACHETOOLS-AUDIT-01-PROTOCOL.md),
[all original attempts](results/cachetools-audit-01/),
[structured review](results/cachetools-audit-01/comparison.json).

One authored request over unchanged selected cachetools5.5.2 source files,
GPT-6 Astra medium, one attempt per condition, fixed baseline→prior→current order.
All three completed without timeout or retry and met all five frozen criteria.
Input includes cached input once; elapsed is full process wall time.

| Condition | Input | Cached within input | Output | Total tokens | Seconds | Criteria |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No skill | 109,499 | 88,832 | 2,304 | 111,803 | 82.797 | 5/5 |
| Prior | 86,607 | 69,504 | 2,916 | 89,523 | 101.780 | 5/5 |
| Current | 85,672 | 62,976 | 3,085 | 88,757 | 108.364 | 5/5 |

Current used **20.6% fewer tokens but 30.9% more time** than no skill. Against
prior it used only0.86% fewer tokens and6.47% more time. Neither skill session
read the optional audit guide/script or invoked `audit.py`: both authored their
own Python runner. The new baseline cache was **not exercised**, so these token
differences cannot be attributed to that optimization. The identical entry body
was present in recorded initial messages and read again by each skill session;
later file reads were not the first exposure. Baseline had no matching body
observation; lack of an exact match does not prove absence of every influence.

## What the original executions establish

Each condition ran two correct-code selected tests once and eight faulty selected
tests. All used unchanged upstream test bodies and isolated mutations within
LRUCache. Baseline recorded copied imports in the actual native process with
verbose imports, plus a separate binding precheck. Skill sessions used local
profile hooks to observe the executing test's copied class binding. No syntax or
import error was counted as fault detection.

| Isolated fault | `test_lru` | `test_lru_getsizeof` |
| --- | --- | --- |
| Read does not refresh recency | Behavioral KeyError, line26 | Pass; gap |
| Overwrite does not refresh recency | Pass; gap | Pass; gap |
| Evict most-recent key | Behavioral KeyError, line19 | Pass; gap |
| Ignore supplied getsizeof | Pass; gap | Assertion failure, line48 |

All three answers distinguished these behavioral errors from setup failures and
correctly reused the two normal observations rather than claiming eight separate
normal runs. All suggested concrete assertions for gaps, including inserting two
keys, overwriting the first, inserting a third, then checking membership without
an intervening recency-changing read. None claimed complete LRU coverage.

Work was unequal: no-skill ran10 unittest processes; prior ran15; current ran16.
The task requested focused assertion **suggestions**. Both skill sessions also
executed them against correct and faulty copies: prior combined default/weighted
overwrite in subtests, while current split them into separate methods/processes.
Those extra checks are useful evidence but were not required to pass the frozen
criteria. Their costs remain included, not subtracted to manufacture parity.
Counts above are unittest processes, not all subprocesses or tool calls.

Original file bytes/modes, HEAD and installed resources remained unchanged;
owned scratch copies were removed and only the eight initial project files were
delivered. Pre-collection staged entries match the initial tree. A pre-session
binary index was not captured, so byte-identical index preservation is not claimed.

## Capture and interpretation limits

Of11 shell outputs, nine match original stored output exactly. One prior CLI
output is a suffix: it lacks the original85-character first correct-test command
label, not the native result. One baseline source-reading output is truncated
in original storage and unmatched; the later actual native audit is present
and exactly matched. The capture matcher's `truncated: false` checks a particular
sentinel and does not recognize this other explicit truncation banner. These
limitations remain visible in the export; nothing was replayed to repair evidence.
Private initial instruction text/raw rollouts are excluded; exposure metadata and
redacted original tool records are retained. The export scan is a limited privacy
check, not a security certification.

One author-selected source-excerpt task, n=1, fixed order, shared host/cache,
unblinded review and unequal work do not establish statistical significance,
causality, independent generalization or all-eight improvement. No representative
chart promotion, production change or release approval follows from this run.
The separate native cache timing evidence remains valid only for its own workload.

한국어: 세 조건 모두 요청한 감사 기준을 충족했다. 수정 스킬은 무스킬보다 토큰을
20.6% 적게 썼지만 시간은30.9% 더 걸렸고, 기존 스킬과의 토큰 차이는0.86%였다.
두 스킬 실행 모두 새 도우미를 사용하지 않아 배치 최적화 효과로 볼 수 없다.
추가 검사를 수행한 작업량 차이와 원본 기록의 일부 잘림도 공개한다. 전체 스킬
성능 개선이나 배포 준비 완료를 입증한 결과는 아니며 대표 그래프는 바꾸지 않는다.
