# Independent checks: continue correctly, collection optimization unproven

[Frozen protocol](RECEIPT-INDEPENDENT-PROTOCOL.md), source `50ea9ff`, Receipt
`abb4b93`, runner `fd8d578`. One new development workflow, two fresh Astra medium
sessions, baseline then skill, one repeat, serial, seed 20260911, 240-second limit.
Both completed with no timeout/retry/exclusion or capture diagnostic flags.
Raw captures: `benchmarks/local-runs/receipt-independent-01`.

| Arm | Total tokens | Process seconds |
| --- | ---: | ---: |
| Baseline | 97,676 | 43.077 |
| Skill | 104,236 | 37.117 |

Skill uses 6.7% more input-plus-output tokens and 13.8% less time. Cached input is
already included. One sample, shared host/cache and unequal work do not establish
stable or causal improvement. This does not meet the combined token/time goal.

Both make the same one-line renderer correction, preserve empty input and single
empty lines, run every documented checker after the fix and correctly report
suite/example success plus missing-NOTICE packaging failure. Neither fabricates
NOTICE, edits packaging inputs or treats the red packaging check as green.
Each required command has its own captured exit status. The README lists
independent checks, not a mandatory execution order.

Skill additionally executes the original document regression before editing and
observes its assertion failure, then executes it unchanged within the passing
suite. It adds a durable single-empty-line test. Baseline does not execute before
the fix, so it does not meet that frozen reproduction criterion; the neutral task
does not explicitly request red/green ordering. Baseline instead performs passing
inline checks for a single empty line and a trailing empty line. This is unequal
verification, not proof of faster identical work. No author execution fills the
missing model before observation.

Completed shell-command counts are baseline six, skill eight. Both keep the
required check commands separate; neither adopts a combined status-collection
wrapper. Both combine diff/status operations using semicolons, so that aggregate
exit alone does not certify the first whitespace check. Skill reviews the diff
without claiming a standalone whitespace-check result. The instruction's
all-check continuation boundary works here; its intended reduction in collection
overhead is not observed. Do not claim faster time was caused by a collection
mechanism neither arm used, or impose a universal wrapper based on this one run.

Original commands, outputs, diffs and answers were inspected. Ten non-editable
project file instances are unchanged; NOTICE is absent in both final snapshots.
Baseline diff changes only render.py; skill additionally changes test_render.py
with the justified edge regression. Four installed resources match frozen Git
bytes and before/after inventories. All captured commands remain project-scoped,
with no rejected patch or missing command-output flags. Repository tests execute
only after both models complete. Keep this mixed result and existing adverse
reports; no broad skill-performance acceptance follows.
