# Recorded usage is not per-command attribution

Inspected original history-regions-01 JSONL, not final-answer estimates. Each arm
has exactly one turn.completed usage record, with no per-command usage records.
The new inspect_usage.py validates this shape rather than summing potentially
cumulative records. Cached input is a subset of input, not an extra charge to add
or a category to remove to make a benchmark favorable.

| Recorded category | Baseline | Skill | Difference |
| --- | ---: | ---: | ---: |
| Cached input tokens | 59,776 | 80,512 | +20,736 |
| Other input tokens | 9,301 | 9,551 | +250 |
| Output tokens | 1,265 | 1,424 | +159 |
| Total tokens | 70,342 | 91,487 | +21,145 |

About 98.1% of the total-token difference lies in the cached-input category. This
does not explain why those inputs were processed or establish a price/latency
effect. All cached tokens remain in the original total metric.

Completed command output is 12,596 versus 11,335 Unicode characters; command text
is 2,454 versus 2,894 characters. Agent-message text is 2,069 versus 2,341 characters
across two versus three completed agent messages. These character counts are not
tokens and omit any unexposed runtime context. Skill's smaller visible tool output
and fewer shell calls do not explain away the higher recorded total.

Consequently this trace does not support attributing the increase solely to longer
skill instructions, repeated source output or shell-call count. Do not create a
per-command cost allocator from these counters or delete verification on that basis.
Continue judging candidate changes through actual behavioral/cost comparisons;
any future finer-grained instrumentation must preserve original totals and disclose
its own environment changes. No runner, model, metric or historical result changed.

Two dedicated tests validate the cache partition and reject ambiguous/missing/
invalid usage. The analyzer reports only counters and limitations, not raw prompts,
source code, credentials or a dollar estimate.
