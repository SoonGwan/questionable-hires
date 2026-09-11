# Referenced audit report: understood correctly, not an end-to-end audit benchmark

[Frozen protocol](CON-ARTIST-REPORT-PROTOCOL.md), snapshot `6754ab8`, entrypoint
`1f8b8b6`, helper/references `6fc0c48`, runner `fd8d578`. One generated task,
two fresh Astra medium sessions, baseline then skill, one sample, serial,
240-second deadline, seed 20260911. Both complete, no timeout/retry/exclusion.
Raw evidence remains private in `benchmarks/local-runs/con-artist-report-01`.

| Arm | Total tokens | Process seconds |
| --- | ---: | ---: |
| Baseline | 68,553 | 30.924 |
| Skill | 51,693 | 32.966 |

Skill uses 24.6% fewer total tokens and 6.6% more elapsed time. Input includes
cached input, with output added once. This is one precollected-report interpretation
task, not audit execution, spontaneous helper adoption, a before/after output-format
comparison or stable performance evidence. Both arms receive identical reference-
format output; do not attribute their difference to JSON output deduplication.

Both interpret actual generated audit results correctly: missing and duplicate
appends survive the existing truthiness test; the same exact-content probe passes
correct code and fails both faulty implementations. The malformed variant fails
import with SyntaxError, not a behavioral assertion; its skipped probes are not
validated. Both resolve later normal-test references as the first successful
observation rather than missing evidence or independent executions. Both propose
an exact-content test starting with an existing item and checking literal True,
and distinguish other untested faults from demonstrated survivors.

Baseline executes four read-only shell commands and emits the report/recipe twice,
the second time with line numbers. Skill uses two commands: discovery, then the
entrypoint and all six project artifacts together. It does not open optional
helper references or rerun an audit. The README explicitly explains JSON Pointer
semantics for both arms, so this does not test unaided format discovery. Both obey
the no-rerun/no-edit request. Original command outputs and final answers were read.

All twelve project file instances remain unchanged; both diffs are empty. Five
installed skill resources match frozen Git bytes and before/after inventories.
No capture diagnostic flags or rejected patches. Report tracebacks retain standard
library paths, while disposable project paths are redacted; a `/private` alias
prefix remains before the placeholder in this frozen generated report. No failure
text or result is changed. Keep the generated cases hash and original captures
for reproduction rather than regenerating and silently substituting evidence.

The author fixture executes the real helper to establish the three records. Those
executions are not credited as work performed by evaluated models. Repository
tests run after both sessions complete. Refreshed-baseline interpretation remains
unit-tested only; this case points to the first baseline. The eight-skill outcome
and efficiency objective remains unmet. Preserve this favorable token observation
alongside its adverse time and narrow-scope limitations.
