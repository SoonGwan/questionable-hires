# History hunk lookup — 2026-09-15

Parent `dd4982f`. Checkpoint 09's history task had no repeated helper reading and
both arms used three shell calls. Its cost increase does not justify removing
needed history or pretending duplicate tool calls caused it.

The optional collector instead has a small internal optimization: sort/deduplicate
selected line numbers once, then use binary search to decide whether a hunk
overlaps. Previously every hunk scanned all selected lines. Returned evidence,
omitted-hunk counts, fallback behavior and safety boundaries stay unchanged.
No skill entry expansion or new mandatory workflow.

## Evidence and limits

[Function benchmark](results/history-hunk-lookup-01/author-benchmark.json): five
calls per version at 1/1,000/10,000 authored hunks, alternating order, exact output
equality. At 10,000 hunks with 100 targets the median is 69.80 → 14.84 ms. At one
hunk it is 3.33 → 3.50 microseconds: keep the small adverse observation. Synthetic
function inputs do not establish typical collector workloads or agent savings.

[Complete collector observations](results/history-hunk-lookup-01/collector-observations.json)
use actual disposable Git repositories and 1.1 MB files, three calls per version:

| Layout | Baseline median | Candidate median |
| --- | ---: | ---: |
| Whole-file rewrite | 274.44 ms | 278.03 ms |
| Scattered edits | 239.46 ms | 237.83 ms |

All JSON evidence is identical; source/status unchanged. End-to-end differences
are small and mixed; no meaningful full-collector gain is established. The native
scattered case attributes only a few selected lines to its many-hunk commit, so
it does not reproduce the function benchmark's 100-target workload. No memory,
model-token, user-experience or whole-eight improvement claim follows.

The collector benchmark now optionally exercises scattered changes while retaining
its original rewrite default. Tests cover empty targets, unsorted/duplicate targets,
zero-new-line deletion hunks, boundaries and fallback, plus existing real Git
rename/shallow/dirty/read-only behavior: 25 tests pass / 7.955s.

Keep this small implementation improvement, but stop optimizing this function as
a proxy for the full goal. The next significant work must concern whole developer
tasks and input/context costs across hires. Historical/featured graphs stay fixed.

## 한국어

이력 분석의 비용 증가를 중복 탐색 탓으로 돌릴 근거가 없어 안내는 그대로 뒀다.
선택 줄과 변경 구간을 대조하는 내부 함수만 이진 검색으로 바꿨다. 큰 문자열
함수 측정은 빨라졌지만 실제 Git 도우미 전체 실행은 차이가 작고 일부 느려졌다.
동일 증거 출력과 테스트 25개를 확인했으며 전체 성능 개선으로 주장하지 않는다.
이 함수의 작은 개선을 전체 목표 대신 반복하지 않고 개발 작업 단위 개선으로
돌아간다. 기존 그래프는 변경하지 않는다.
