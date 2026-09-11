# Receipt profile transfer: evidence reuse adopted, efficiency still unmet

[Frozen protocol](RECEIPT-PROFILE-PROTOCOL.md), source `805298a`, Receipt `7056153`.
Four fresh Astra medium sessions: gated skill, direct skill, direct baseline,
gated baseline. Two related development tasks, one sample per arm, serial,
240-second deadline, seed 20260911. All complete without timeout/retry/exclusion.
Raw original captures remain private in `benchmarks/local-runs/receipt-profile-01`.

| Case | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| Direct suite | 80,268 / 27.207 | 120,890 / 40.097 |
| Opt-in archive profile | 97,543 / 36.499 | 120,221 / 47.618 |
| Sum | 177,811 / 63.706 | 241,111 / 87.715 |

Skill totals are **35.6% more tokens and 37.7% more elapsed time**. Tokens include
input (cached input already included) plus output. Shared host/cache and one sample
do not give stable estimates. Both skill sessions have a rejected patch, further
preventing causal attribution to the current instruction. No predecessor arm:
this cannot measure the latest edit's isolated effect. Repository tests ran only
after all four model sessions finished.

## What changed in behavior

All four sessions make exactly the same one-line numeric-sort correction, retain
the complete tests and configuration, and demonstrate actual file assembly failing
before and passing after. Direct arms execute the unchanged suite before/after.
Gated arms enable ARCHIVE_CHECKS for both the failing and passing observations;
after the fix they also run the default suite, retaining its one expected skip.
Neither arm mistakes the default green/skipped result for long-document evidence.
Assertions, README and requirements are byte-identical in all twelve retained
file instances. All final project diffs contain only the sorting line.

Both skill sessions explicitly select the unchanged suite as their after evidence.
Neither separately reruns the included regression. This is observed adoption of
the current rule, unlike [the previous URL collection traces](RECEIPT-COLLECTION-01.md),
not proof that the wording caused the change across different tasks. The gated
default run checks a different configuration/skip policy and is not counted as an
identical-regression duplicate. Baseline follows the same sound testing pattern.

Completed shell commands: direct baseline 4 / skill 7; gated baseline 6 / skill 8.
Each skill does three discovery/read commands, a before suite, separate whitespace
and focused diff/status commands, and its after suite(s). Baseline combines its
third requirements read with before execution. Direct baseline also combines its
final checks; gated baseline keeps default and enabled suite commands separate.
No history traversal, revision lookup, optional helper/reference read or parent-
directory discovery appears in these captured commands. More prose telling Receipt
to reuse tests would not address the remaining observed work.

## Integrity, limits and next direction

Both skill stderr logs report one outside-project patch rejection with no captured
target. Final correct scoped changes cannot establish all attempted actions were
scoped. Do not assume a path-alias cause, discard rejected attempts, or attribute
their whole cost to the skill. Baseline has no rejection. Empty skill command
outputs are the successful whitespace checks; no invalid JSON, non-object JSON or
model-error event flags. Eight installed resource instances match frozen Git bytes
and are unchanged before/after. Original commands, outputs, diffs and answers were
read; no author replay is represented as model execution.

Retain the coverage-reuse distinction without claiming overall acceptance. Do not
add another mandatory collection rule based on these command counts: the previous
collection instruction did not achieve that result. Separate actionable repeated
task work from rejected-patch/tool-boundary overhead before changing instructions.
The next substantive optimization should target a demonstrated unresolved execution
cost, not run more variants of these exposed single-line fixes until one wins.
