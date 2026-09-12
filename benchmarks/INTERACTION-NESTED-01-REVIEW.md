# Nested discovery: favorable costs, different coverage

[Inspect the exported commands, tests and answers](results/interaction-nested-01/README.md).

[Frozen protocol](INTERACTION-NESTED-01-PROTOCOL.md), revision `c74cdf8`.
Both sessions completed without outer timeout. No retries or exclusions. Private
original traces: `benchmarks/local-runs/interaction-nested-01/`.

| Arm | Input + output tokens | Process seconds | Discovery commands |
| --- | ---: | ---: | ---: |
| Baseline | 84,515 | 53.960 | 3 |
| Skill | 70,416 | 47.777 | 2 |

Skill costs are **16.68% fewer tokens / 11.46% less time**. Cached input is already
included (baseline 74,624; skill 61,184), and reasoning output is not added twice.
One exposed synthetic pair, shared host/cache, fixed order and unequal additional
coverage prevent a broad or causal improvement claim.

Both read the nested AGENTS.md and documented entrypoint, import actual Search,
retain only `apps/catalog/qa/test_search.py`, and execute the documented runner
from the catalog directory. All six original fixture files are byte-identical
afterward. Actual outputs show empty-query normal behavior passing and reversed
nonempty completions failing on stale overwrite, not an import or timeout error.
Both runner results retain child exit 1, timeout false, cleanup complete true,
and output truncated false. No installs or external actions appear in commands.

The skill lists hidden project paths once, then reads its entrypoint and all
located project instructions, requirements, source and runner in one command.
The baseline first lists selected visible paths, then widens to hidden paths and
reads project documents/source, then reads the runner and lists the catalog.
This supports successful inventory reuse, not proof that the instruction edit
caused the measured cost difference. The baseline's widened search is legitimate
coverage of locations omitted in its first query, not automatically wasted work.

Coverage differs: skill exercises in-order and reversed nonempty overlap as two
subtests plus an empty-query normal transition. Baseline exercises a longer normal
sequence and two reversed overlaps, one with a nonempty latest query and one with
a cleared latest query. Baseline therefore also captures stale results after
clearing; skill does not test that overlapping-empty case. Both satisfy the frozen
required categories, but they do not do identical work. Skill relies on the outer
three-second process deadline; baseline additionally uses 0.5-second async waits.
Both clean up owned tasks. Browser behavior remains untested.

Keep the discovery candidate: required nested instructions and behavior were not
lost in this screen. Do not rerun this unchanged fixture for a stronger number or
promote it as all-eight efficiency evidence. Representative repository transfer
and broader interaction coverage remain open.
