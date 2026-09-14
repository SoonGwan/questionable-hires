# Shared collection for distant ranges — 2026-09-15

Parent: `671128e`. Optional Necromancer helper capability, not a new model result.
The [preceding model screen](results/history-invoice-01/README.md) remains adverse
and did not use this helper. This change does not explain or rescore that run.

## What changes

Repeat `--lines` for relevant disjoint ranges in one file, or use
`trace_ranges(repo, filename, [(5, 5), (40, 40), (75, 75)])`. Current source,
repository identity/status and blame are collected once; shared commits are shown
once with all selected historical regions. Gaps are not selected. Sorted union
semantics deduplicate overlapping/adjacent ranges without mutating input.

The existing `trace(repo, filename, start, end, max_commits=3)` and single-range
CLI result shape remain compatible. Disjoint selections add `ranges`. The 100-line
cap is global, as are commit/patch caps; selecting several origins can omit more
commits than independent calls with a separate cap each. Omission counts remain
visible, not treated as complete history. No persistent cache or stale-result
reuse, broader source limit, fetching, external tools or skill-entry growth.

## Actual controls and measurement

Five new tests cover shared collection, repeated CLI flags, mixed list/tuple
ranges, union bounds, invalid input, rename plus dirty attribution, and the global
commit cap. A real three-region commit requires **12 Git commands separately /
4 batched**. Selected current/blame rows are identical; all three old/new changes
remain in the shared patch, and an irrelevant gap does not appear. Repository
bytes, including Git files, remain unchanged. A three-commit selection limited
to one patch still reports two omitted commits and all selected attribution.

Before implementation, the new CLI assertion observed only the last range
(`[40]` rather than `[5, 40, 75]`); four tests reported missing `trace_ranges` API.
These establish unsupported new behavior, not four pre-existing analysis bugs.
After implementation, all five new tests pass.

[Raw local measurement](history-ranges-01-local.json) executes the previous
collector from `671128e` three times per round and the candidate once with three
ranges. It uses one 1.1 MB, 100,000-line authored Git file, 30 selected lines,
three alternating-order rounds, complete Python/Git subprocess cost included.
The source hash and candidate bytes are retained; no model is involved.

| Measure | Separate calls | Batched ranges |
| --- | ---: | ---: |
| Median complete collection time | 0.358508s | 0.115873s |
| Captured stdout bytes | 9,339 | 7,878 |

This is **67.68% less local collector time** and **15.64% fewer output bytes**,
not model tokens or whole-task savings. Each round verifies identical selected
current/blame records, retained old/new patch lines, no omitted/truncated commits
and unchanged source. Full JSON differs deliberately: separate calls duplicate
metadata while batching shares it and records the ranges. Timing is one local
fixture, n=3, and does not establish a general benefit or a memory bound.

Reproduce on the candidate checkout with a new output path:

```sh
python3 -B -m unittest discover -s tests -p test_history_ranges.py
python3 -B benchmarks/benchmark_history_ranges.py --baseline-revision 671128e \
  --output benchmarks/local-runs/history-ranges-replay.json
```

The guide still allows native Git for simple facts. Adoption and whole-task
efficiency require fresh behavioral evidence; no featured charts change here.

## 한국어

같은 파일의 떨어진 여러 구간을 한 번에 조사하도록 선택형 도우미를 확장했다.
사이의 무관한 줄을 끼워 넣지 않고, 저장소 상태·출처·공통 커밋 수집을 공유한다.
실제 세 구간 검사에서 Git 실행은 12회에서 4회로 줄었고 필요한 변경은 유지됐다.
10만 줄 로컬 이력의 전체 도우미 실행 중앙값은 0.359초에서 0.116초로 감소했다.
이는 모델 전체 작업의 67.68% 절감을 뜻하지 않는다. 커밋 제한은 전체 선택에
공유되므로 빠진 근거를 확인해야 하며, 기존의 불리한 모델 결과와 그래프는 유지한다.
