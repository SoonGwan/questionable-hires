# Bulk history: correct decisions, mixed efficiency, no helper adoption

Four fresh Astra medium sessions follow the [preregistered protocol](HISTORY-BULK-PROTOCOL.md)
at snapshot `1253f8b`: two development cases, baseline/skill, one repeat, serial
balanced order, no retries or exclusions. Raw ignored evidence lives under
`local-runs/history-bulk-01`; the generated cases are
`local-runs/history-bulk-cases-01.json`, reproducible from the committed builder.

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| Active fallback | 118,261 | 97,935 | 45.124 | 38.231 |
| Normalized caller | 90,347 | 102,701 | 43.485 | 43.263 |
| Sum | 208,608 | 200,636 | 88.609 | 81.494 |

Input includes cache; total tokens add output once. The sum changes by -3.8%
tokens / -8.0% time. The normalized control instead costs +13.7% tokens with
essentially unchanged time (-0.5%). These are single observations, not confidence
intervals or a demonstrated stable improvement. The aggregate is not the original
chart's mean-of-task-ratios statistic.

## Equivalent requested outcomes

All four correctly identify compatibility commit
`6bc327bf410a2ddece1557cb791c7a5ced828e5c`, inspect the current caller and supported
contract, and execute the real renderer for missing, empty and nonempty display.
Both active reviews retain the fallback: an in-memory proposed replacement raises
KeyError for missing display and returns an incorrect empty string for empty
display; the nonempty case stays correct. Both normalized reviews allow removing
only the private helper fallback while preserving caller normalization. Current
and proposed renderer tests pass all three inputs in both normalized sessions.
No implementation or project edits were requested or produced.

Original commands and behavioral output, not just final prose, were inspected.
Active arms run the existing tests on current code and print the actual proposed
renderer results; normalized arms run tests on both implementations. Baseline
normalized additionally asserts pairwise result equality; skill normalized relies
on the existing expected-value assertions for both. Both support the frozen
contract, without claiming identical execution detail.

## Work actually performed

Neither skill session reads the helper reference or runs `trace.py`. The new
large-hunk excerpt therefore has **no demonstrated model adoption or causal
efficiency benefit** here. Do not force the optional helper into this fixture.

Active skill uses focused line blame, pickaxe and a tail of the relevant patch,
with five completed shell commands versus baseline's six. Baseline initially
reads multiple full historical outputs and later filters out generated comments.
Normalized skill instead reads the whole current file and whole-file blame,
then repeats focused blame and reads a full patch: four commands versus baseline's
five, yet more tokens. Baseline also reads excessive history, then filters it.
Fewer commands alone do not explain or ensure savings. No per-command model token
accounting or controlled causal attribution is available.

## Integrity and disposition

All sessions complete with exit zero and no timeout, rejected patch or capture
diagnostic flags. The eight installed resource instances match snapshot blobs
and before/after inventories. All sixteen original project-file instances match
the fixture bytes; final diffs are empty. Inspected completed commands stay within
project boundaries and use memory-only substitutions. Clean final snapshots do
not prove every transient action, and clean capture flags do not prove complete
capture of large outputs. The decisive behavioral output is present in the
original captures; no author replay is counted as model verification.

Retain these mixed results, not an acceptance claim or replacement headline chart.
The collector's local evidence-selection regression remains fixed, but the tested
workflow does not need it and its adoption benefit is unverified. Repeated broad
source/history reads remain a concrete efficiency issue even in correct runs.
Do not rerun this exposed pair merely to obtain favorable scores. Broader
representative and independent confirmation work remains necessary for the
eight-skill objective.

Repository regression after the experiment: 138 tests pass (14.293 seconds),
including the actual-Git fixture and installed resource checks. Documentation
validation and whitespace checks also pass; these are not model-quality scores.
