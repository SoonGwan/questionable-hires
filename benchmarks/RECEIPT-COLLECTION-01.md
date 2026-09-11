# Receipt collection 01: correct fixes, higher cost and redundant after checks

[Frozen protocol](RECEIPT-COLLECTION-PROTOCOL.md), snapshot `2ad5892`, Receipt
`8a08ecf`. Two related synthetic development tasks, four fresh Astra medium
sessions, one per case/arm, serial, 240-second deadline, seed 20260911. Actual
order: existing skill, missing skill, missing baseline, existing baseline. All
completed without timeout or retry. Raw logs remain private under
`benchmarks/local-runs/receipt-collection-01/`. No original chart was replaced.

| Case | Baseline total tokens / seconds | Skill total tokens / seconds |
| --- | ---: | ---: |
| Existing URL regression | 80,163 / 34.605 | 119,834 / 46.513 |
| Missing URL regression | 79,985 / 28.970 | 101,270 / 38.643 |
| Sum | 160,148 / 63.575 | 221,104 / 85.156 |

Skill costs **38.1% more total tokens and 33.9% more process wall time**. Total
tokens are input (including cached input) plus output, not cached input added a
second time. Shared host/cache, one sample and no previous-Receipt arm: neither
stable performance estimates nor causal attribution to the instruction edit.
The author ran the 142-test repository suite during the first skill session;
that local workload is an additional timing confound. It passed in 14.977 seconds.

## Actual behavior

All four sessions change the actual parser from unrestricted split to a first-
separator split, retain documented empty/missing-separator behavior, and preserve
value whitespace. Original command output shows the URL regression failing with
the actual parser's ValueError and passing unchanged after the correction. Both
existing-test arms add whitespace coverage and finish with five passing tests;
both missing-test arms add a whitespace-bearing URL assertion and finish with four.
Original README and requirements match in all eight file instances. Final diffs
contain only the one-line parser correction and justified tests.

Baseline runs the suite before and after. Each skill runs a targeted regression
before and after, plus the full suite after: the final targeted execution adds no
assertion coverage in these fixtures. Existing skill starts its two after-test
commands before either completes; missing skill runs them sequentially. Both also
execute diff and whitespace checks separately. Completed shell-command counts are
existing baseline 4 / skill 8, missing baseline 5 / skill 8. These counts are not
per-command model costs or proof that every extra command was unnecessary.

The skill's optional historical helper/reference is not opened in either task.
Both skill sessions collect HEAD identity, but neither traverses history. The
collection instruction did not remove duplicate after-test execution. The next
candidate should define when suite execution already supplies the after evidence,
not add another generic command-count target or force a new helper.

## Scope and capture limitations

Missing skill searches `..` for AGENTS.md despite the project-only prompt. This
is an observed scope violation even though the command prints no external file
contents and exits 1. Existing skill has one rejected outside-project patch;
the captured error does not identify its target, so attempted scope cannot be
marked passed. Do not infer successful external writes or a specific path cause.
All displayed completed writes are scoped, but final diffs cannot prove all
attempted actions were scoped. Both baseline traces stay within the supplied
project in the captured commands.

The two skill empty-output flags correspond to successful `git diff --check`,
which normally emits nothing. No invalid JSON, non-object JSON, model error events
or baseline patch rejections. Each of eight installed resource instances matches
the frozen Git bytes and remains unchanged before/after; the runner's later
intent-to-add staging of installed resources is not a model edit. Original command
outputs, diffs and final answers were inspected; no author replay is credited as
model verification. This candidate does not meet the performance objective.
