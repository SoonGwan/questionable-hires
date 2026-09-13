# All-eight explicit-contract gate: time/token tradeoff, not acceptance

[Detailed behavioral review](../../BUNDLE-CONTRACT-03-REVIEW.md),
[frozen protocol](../../BUNDLE-CONTRACT-03-PROTOCOL.md), [run](run.json),
[all cell metadata](summary.json). Launch revision `b73ca09`, resources `557f012`.
Nine exposed authored tasks, eight skills, Astra medium, one baseline/skill cell
each, serial shuffled schedule. All 18 completed; no retries/exclusions/timeouts.

| Task | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| boundary-fix | 80,626 | 84,858 | 32.270 | 34.536 |
| formatter-review | 78,974 | 67,406 | 29.218 | 35.264 |
| history-active | 64,067 | 85,707 | 29.741 | 38.354 |
| necessary-state | 66,125 | 87,653 | 82.667 | 74.982 |
| persistence-test | 85,514 | 145,730 | 72.256 | 67.070 |
| rolling-schema | 105,281 | 93,326 | 103.785 | 47.738 |
| search-diagnosis | 100,521 | 71,776 | 75.194 | 58.403 |
| search-order | 82,041 | 106,179 | 62.192 | 65.106 |
| search-protected | 65,717 | 104,085 | 62.056 | 59.629 |
| **Sum** | **728,866** | **846,720** | **549.379** | **481.082** |

**+16.17% tokens / −12.43% summed process time.** Ratios of sums, not equal-task
mean ratios. Tokens are input (cached input included once) plus output; reasoning
output is not double-counted. Six of nine skill cells use more tokens; four take
longer. This does not meet similar/lower token cost with substantial real-work gain.

Both arms establish the requested core functional/review outcomes in the inspected
evidence, but **necessary-state baseline searches outside the project** with
`find ..`. It remains a scope failure included in all costs, not an excluded cell.
Extra work differs: skill duplicates QA sequences for retained delivery; Con Artist
reads helper internals and builds binding support; several baselines retain extra
reports/logs or perform extra verification. See the per-cell review, not just totals.

Original terminal usage, redacted event records and installed resource inventories
are reconciled. Full small final projects, commands, source hashes, answers and
diffs are exported for every cell. `source-sha256.json` hashes original artifacts,
not redacted export bytes. Empty-output flags and the missing persistence heading
are explained in the review, not hidden. No author replay replaces model evidence.

This is an exposed synthetic development gate with revised visible obligations,
n=1, shared host/cache and fixed order. It is neither independent real-repository
confirmation nor causal isolation of a skill change. Do not compare directly with
the older differently worded gate as a controlled improvement. Earlier adverse
results and featured/localized graphs remain unchanged; no public release follows.

Post-run author validation: **358 tests pass (49.783 seconds)**; catalog and
featured synchronization checks pass. Export privacy scan found no unredacted
home/macOS temporary-root paths. Original fixture bytes are preserved outside
authorized implementation targets; both arms' final Form and eligibility fixes
match. These checks do not turn the observed tradeoff into performance acceptance.
Staged whitespace check flags two native unittest progress lines in the baseline
`qa-search-output.txt` artifact; their original trailing spaces are preserved as
evidence rather than silently reformatted. Authored documentation has no such errors.
