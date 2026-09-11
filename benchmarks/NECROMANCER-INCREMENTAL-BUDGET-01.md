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
