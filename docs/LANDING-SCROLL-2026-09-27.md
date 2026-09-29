# Evidence table position across languages — 2026-09-27

Baseline `0cb51640`. Previously, changing language replaced experiment markup and
preserved the metric and details openness, but reset both evidence tables' horizontal
positions. At390px the same real browser fixture observes featured0.4→0 and
checkpoint1→0. These are scroll progress fractions, not benchmark resource ratios.
[Original failing observation](../benchmarks/results/landing-scroll-0cb51640/before.json)
is retained.

The fix captures each table's relative horizontal position immediately before the
accepted translation replaces the markup, then restores it after translated
content/layout updates. This includes movement while the request is pending and
keeps the right edge even if translated column widths differ. The existing stale
request guard is retained. No benchmark data, graph arithmetic or palette change.

[Unchanged browser fixture](../benchmarks/results/landing-scroll-0cb51640/check.cjs)
holds the EN translation response, moves both open tables while waiting, releases
the response and checks both positions. It then returns to cached KO and checks
positions, openness, selected time graph, no page overflow or script errors.
[After observation](../benchmarks/results/landing-scroll-0cb51640/after.json) passes:
both0.4/1 positions retained in each direction. [Source/fixture identities](../benchmarks/results/landing-scroll-0cb51640/source.json)
record exact hashes. Closed-table historical positions and arbitrary translation
failure paths are not new claims. The original preview coordinator is retained;
its existing temporary script/runtime paths must be available when reusing it.
The browser fixture itself accepts an explicit site URL and output JSON path.

All12 existing landing tests,15 generated-file check and featured synchronization
check pass. This is local failing-before/passing-after behavior, not a model cost
comparison or hosted release assertion. Public delivery is recorded separately.

## Hosted delivery

Release `cd9de7ce` is live on the dedicated Mac/Cloudflare origin. The same held
translation/cached-return fixture passes against ordinary public URLs at390px.
[Public outcome](../benchmarks/results/landing-scroll-public-cd9de7ce/result.json)
retains both table positions in both directions, no page errors and the original
neighboring assertions. [Release/source audit](../benchmarks/results/landing-scroll-public-cd9de7ce/audit.json)
records public health and byte-for-byte matching of the served app.js to the fix.
The original failing/local passing observations remain unchanged; hosted checks
do not relabel them or alter any graph measurement.

한국어: 언어 전환으로 표 HTML이 교체되면서 두 표의 가로 위치가0으로 돌아갔다.
실제 브라우저의 동일한 검사에서 수정 전 실패·수정 후 통과를 확인했다. 번역
대기 중 이동과 캐시된 언어로 복귀할 때 열린 표의 위치·그래프·펼침 상태를
유지한다. 기록의0.4·1은 UI 스크롤 비율이며 실험 성능 수치가 아니다.

공개 릴리스cd9de7ce에서도 동일한 검사가 통과했고 실제 제공된 JS가 수정본과
일치한다. 원래 실패 기록과 로컬 통과 기록은 그대로 보존했다.
