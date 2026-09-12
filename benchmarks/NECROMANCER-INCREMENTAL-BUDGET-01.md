# Incremental excerpt budgeting

The selected-patch helper previously rebuilt and sorted the entire candidate
excerpt for every neighboring row considered. It now tracks the exact rendered
character count and sorted selected indices. Inserting a row replaces one gap with
two: account for the row/newline and the change in omission-marker count. Initial
and final render remain; complete patch parsing and tail validation are unchanged.
No evidence, target-first priority, context selection order or budget is removed.

Run: `python3 -B benchmarks/benchmark_history_excerpt.py --baseline-revision 0e3c790`.
Candidate helper SHA-256:
`5166a6dd692c1f124aca9cef79f774f4490df4da6b66aae962757df781169c8d`.
Python 3.9.6, existing 100,000-row input and five target distributions, seven
alternating-order calls per version/case, exact full excerpt equality each time.

| Targets | Old median seconds | New median seconds |
| --- | ---: | ---: |
| One | 0.082040 | 0.082916 |
| 20 nearby | 0.082692 | 0.083141 |
| 20 distant | 0.089132 | 0.085644 |
| 100 nearby | 0.086044 | 0.086703 |
| 100 distant | 0.125622 | 0.085987 |

The distant-100 case is about 31.6% faster; nearby cases are slightly slower
(approximately 0.5–1.1%). This is local function timing, not complete Git collection,
model tokens or end-to-end performance. Full raw patch parsing remains linear;
the change removes repeated rendering during neighborhood selection.

A new independent full-render oracle checks every integer budget from zero through
full output length for five target layouts, including both ends, merging gaps,
adjacent targets and Unicode text. Existing deletion, malformed-tail, multiple-hunk,
dirty-worktree and history safety tests remain. Structural validation alone would
not establish this arithmetic's correctness.

All 166 repository tests pass in 21.173 seconds, including 21 history-helper tests;
skill/repository validators and diff checks pass. No model benchmark was run for
this helper change, and the broad eight-skill efficiency objective remains unmet.

## Whole collector follow-up

Existing benchmark_history_collector.py against 0e3c790 uses actual disposable Git
history, a 1,100,000-byte current file and lines 50000:50099. Complete JSON is
identical for all six processes. Baseline seconds: 0.327659083, 0.327986833,
0.328813584; candidate: 0.335589125, 0.327824750, 0.326768083. Medians are 0.327987
and 0.327825: essentially unchanged. This contiguous-target fixture does not support
extending the distant-target microbenchmark gain to complete collector performance.
Input SHA-256 remains cde29c379cb2b3421e49058685ffe928852332f3852c49a99c31a558e4a4f4d5.

A separate seeded (20260911) comparison generated 100 mixed insertion/deletion/
context patches with Unicode and varying line lengths. Seven budgets, each with
valid and malformed-tail variants, yielded 1,400 exact matches against 0e3c790.
This supplements, not replaces, the committed full-render budget oracle.

Profiling a single-target 100,000-row patch shows 100,001 re.fullmatch calls and
100,001 regex-cache lookup calls, despite almost every row being patch data rather
than a hunk header. Under cProfile these account for 0.048 cumulative seconds of
0.122 total; profiler overhead prevents treating that fraction as a speedup promise.
Next inspect a header-prefix gate while retaining malformed-header/tail rejection.
No additional implementation change was made during this follow-up.
