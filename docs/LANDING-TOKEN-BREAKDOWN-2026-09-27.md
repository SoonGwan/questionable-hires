# Landing cumulative token breakdown — 2026-09-27

Landing source/release `1acaf4a4`. Measured skill resource remains `75183f2f`;
this is a reporting change, not a skill optimization or new model experiment.
[Original16 comparison records](../benchmarks/results/all-eight-current-05/comparison.json)
and [cost review](../benchmarks/ALL-EIGHT-CURRENT-05-COSTS.md) are unchanged.

| Integration05 sum | Without skills | With skills |
| --- | ---: | ---: |
| Input |592,509 |705,328 |
| Output |13,846 |13,419 |
| Total input + output |606,355 |718,747 |
| Cached input, already included in input |530,432 |613,632 |
| Recorded model responses |38 |39 |

The bilingual expanded comparison now derives every breakdown from the frozen
records. Cached input is a subset of each response's input, not an additional
term or a once-per-task count. Repeated conversation/tool context is included
again when sent as the next response's input. Counts do not estimate billing.
Input increases112,819 while output decreases427; total increases112,392.
These differences describe usage; they do not establish a causal explanation.
Whole-task tokens/time remain adverse: +18.54%/+9.06%.

Verification:16 landing/server tests pass, including rejection of cached input
larger than input and zero recorded responses. Generated build and featured
synchronization checks pass. The existing browser controller verifies14 expanded
layouts across both languages, all8 rows, identical frozen downloads, language
state and root modifier navigation. Actual public HTTPS Chrome checks at390px
verify every breakdown in Korean/English and no page errors or page overflow.
The deployment verifies both origin and public release identity. Local temporary
preview was stopped. No new whole-team efficiency, remote installation or hosted
CI result is claimed.

Public mobile screenshots and the executed controller are retained under
[landing-token-breakdown-1acaf4a4](../benchmarks/results/landing-token-breakdown-1acaf4a4/).

한국어: 누적 토큰 수치를 바꾸지 않고 입력·출력·캐시 입력·응답 횟수를 공개했다.
캐시 입력은 각 응답의 입력에 이미 포함되며 별도로 더하지 않는다. 한·영 공개
사이트의 실제390px 화면과16개 로컬 검사를 확인했다. 전체 스킬의 토큰·시간
절감 목표는 아직 달성하지 못했다.
