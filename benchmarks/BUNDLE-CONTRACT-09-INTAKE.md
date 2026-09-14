# Checkpoint 09 intake — 2026-09-14, review pending

Launch `3a7d972`, skill resources `9071a1c`;
[frozen protocol](BUNDLE-CONTRACT-09-PROTOCOL.md). All 18 scheduled sessions ended,
without retries, timeouts or account-limit interruption. Timing ended at
2026-09-14 14:21:02 UTC. Raw artifacts are retained locally under
`benchmarks/local-runs/bundle-contract-09`; publication and behavioral review
are pending. This is not a completed benchmark review or release gate.

## Verified collection and arithmetic

For all 18 cells, original `turn.completed` usage matches metadata, redacted events
match original streams, installed skill bytes/modes match the launch revision,
before/after installed resources agree, and retained pre-collector index hashes
match the local binaries. Frozen case SHA matches the manifest/protocol. These
checks do not prove complete tool-output capture or task correctness.

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| Boundary fix | 80,064 | 84,448 | 60.289 | 33.998 |
| Formatter review | 79,963 | 49,637 | 34.641 | 28.970 |
| Active history | 63,725 | 67,142 | 26.243 | 33.129 |
| Pending form | 66,691 | 96,674 | 82.211 | 73.413 |
| Persistence audit | 82,917 | 73,571 | 69.594 | 36.635 |
| Rolling schema | 65,363 | 70,118 | 50.518 | 69.323 |
| Search diagnosis | 122,168 | 71,521 | 112.027 | 57.910 |
| Search-order QA | 100,683 | 72,247 | 70.250 | 65.292 |
| Protected QA | 99,291 | 71,686 | 67.149 | 62.313 |
| Sum | 760,865 | 657,044 | 572.922 | 460.983 |

Ratio of sums: **13.65% fewer tokens, 19.54% less process time** in the skill arm.
Input includes cache once, plus output. All scheduled cells are included. Four
pairs use more skill tokens; history and schema are worse on both resource axes.
These are unadjusted observations, not accepted efficiency wins: exposed authored
tasks, n=1, shared host/cache, unequal work and pending evidence review limit them.

## Original evidence issue already located

Pending-form skill item 8 chains native unittest, asset comparison, diff checks
and status with `&&`. Captured output contains the final implementation diff and
status, **not native test identities, assertions or a test-count summary**. Exit
zero and the final answer cannot supply the missing native evidence. Record this
as an original evidence gap; later author replay cannot fill it.

Other empty-output candidates are not equivalent: form item 6 and both search QA
item 5 commands copy support assets and ordinarily print nothing. Diagnosis
baseline item 6 redirects output to a result file; subsequent capture/file review
is still required before deciding whether its evidence is sufficient. Do not
count every empty output as a failure or every nonempty output as complete.

Remaining work: review all original commands/answers, complete project inventories
and allowed changes; replay retained tests against original/final/adverse and
valid-control implementations; inspect intended failures versus setup errors;
reconcile exported artifacts and publish the complete pair review. No charts,
featured pointer, historical measurements or success scores change at intake.

## 한국어

18세션 모두 종료됐고 원본 사용량·스킬 파일·수집 전 인덱스 해시를 대조했다.
합계는 기본 760,865토큰·572.922초, 스킬 657,044토큰·460.983초다.
관측상 토큰 13.65%, 시간 19.54% 감소했지만 아직 성능 향상 판정은 아니다.
4개 과제는 스킬이 토큰을 더 썼고, 이력·스키마 과제는 시간도 더 걸렸다.

폼 과제 스킬 실행에는 최종 diff/status만 있고 원본 테스트 이름·결과·개수가
빠진 출력이 있다. 작성자 재실행으로 이 누락을 채우지 않는다. 모든 과제의
실제 작업·보존 범위·결함 검출·정상 대조군 검토와 공개 결과 대조가 남았다.
기존 그래프는 유지하며, 이 문서는 수집 확인 기록이지 완료된 평가가 아니다.
