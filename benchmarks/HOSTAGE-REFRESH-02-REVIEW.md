# Refresh-owner 02 — evidence recovered, token cost regressed

2026-09-15; [frozen protocol](HOSTAGE-REFRESH-02-PROTOCOL.md), launch `b237aae`,
measured resources `0a94dab`. Four fresh completed sessions, no model retry,
timeout or account limit. Same exposed two development tasks, n=1 per arm.

| Variant | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| a | 110,552 / 138.322 | 193,521 / 123.064 |
| b | 91,270 / 123.097 | 126,499 / 122.587 |
| Sum | 201,822 / 261.419 | 320,020 / 245.651 |

Input (already includes cache) plus output. Ratio of sums: **58.57% more tokens,
6.03% less time**. Both token pairs regress. This is not a performance win,
independent confirmation, confidence interval or evidence about all eight skills.

## Original evidence

Both skill sessions use dedicated native test commands and capture all eight
test results, summary and process exit 0. Faulty a also captures eight tests with
five intended pending-state failures before the production fix (item_9), then
passes after it (item_11). Valid b captures eight passes in item_8. Final reports
match this native evidence, unlike the two missing transcripts in run 01. This
is a useful observed reporting improvement, not proof of a capture-system cause.

Baseline a captures seven tests with seven pending-state failures, then seven
passes (item_6 / item_8). Baseline b initially has three cancellation-harness
failures, repairs its test harness, then captures six passes (item_5 / item_8).
Verbose-header diagnostics flag both baseline failing runs because subtest output
joins method names on a line; the actual names, failure details and native totals
are present. The final passing runs contain all method names. No missing native
summary is found in these reviewed test commands. Test counts are not directly
comparable quality scores; the suites group scenarios differently.

All four retained production files equal the same correct latest-generation
cleanup implementation. Variant b remains unchanged. Frozen requirements and
owner notes are unchanged, installed skill resources remain stable, and both
copied helpers match the measured asset bytes.

## Cost investigation

Recorded shell command counts are baseline a/b: 6/5, skill a/b: 12/7. Counts do
not establish causal token attribution. Skill a separately runs discovery, `ls`,
resource reads, status, another instruction search, copy, two tests, integrity,
diff check and final review. Skill b also repeats inventory and includes a full
new-test diff in its final output. Both read the entire 5,388-byte helper alongside the
entrypoint, not only its usage docstring. Baseline b spends work repairing a
cancellation test; baseline a and skill a both demonstrate pre-fix failure.
Keep these work differences visible rather than attributing all cost to one edit.

The next optimization target is these unnecessary read/review round trips while
retaining independently inspectable test evidence. Do not restore combined test
and Git commands merely to improve a cost number. No additional skill change is
being claimed as measured by this run.

## Separate controls and publication

[Author replay](results/hostage-refresh-02-controls/author-replay.json): all 16
expected outcomes. Each retained suite accepts final production and an alternate
valid generation increment of two, detects unconditional cleanup with actual
False-is-not-True assertions, and each final production passes the independent
six-method oracle. No setup errors or process timeouts; original projects remain
unchanged. Narrow controls do not prove every possible behavior or production
readiness. The replay program now pins both full launch revisions and the native
method counts for each; run 01 output remains untouched.

[All four exported cells](results/hostage-refresh-02/run.json) include native
commands/events, answers and complete retained project text. Raw turn usage
matches metadata; export events/project text and filename sets reconcile to
redacted originals, and source SHA-256 records match. Home/temp/key-pattern scan
has no matches, not a universal secret-detection guarantee. Historical and
featured charts remain unchanged. Detailed test-path/cleanup review and a
prospective cost correction remain next work; no strict full-contract score yet.

## 한국어

명령 분리 후 스킬 두 세션 모두 실제 테스트 결과·종료 코드를 남기고 그 근거로
보고했다. 오류 과제의 수정 전 실패도 보존했다. 그러나 기본 모델 대비 토큰은
58.57% 증가했고 시간은 6.03% 감소에 그쳤다. 성능 개선 달성으로 인정하지 않는다.
별도 정상·오류·정상 대안·정답 테스트 대조 16회는 예상대로 동작했으며 원본과
재실행을 분리했다. 명령 반복·도우미 전체 읽기·새 테스트 전체 diff가 비용 개선
후보다. 테스트 근거는 유지하면서 불필요한 왕복을 줄이는 작업이 남았다.
같은 개발 과제 반복 1회이므로 일반화나 전체 8개 스킬 우위를 주장하지 않는다.
