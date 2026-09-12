# Unrelated-request routing: no observed unnecessary activation in two cases

[Protocol](ROUTING-NEGATIVE-PROTOCOL.md), runner/fixture `ebceca6`, all eight
skill resources frozen at `bead33d`. Two fresh Astra medium auto sessions,
serial, one per task, 240-second deadlines, no retries/exclusions. Nine discovered
personal skills disabled per session; runtime instructions remain. The installed
bundle contains 27 files per session; all match frozen Git hashes and final
inventories. No host installation or external publication was performed.

| Request | Input + output tokens | Seconds | Commands | Observed skill-body reads |
| --- | ---: | ---: | ---: | ---: |
| Explain pure formatting | 47,551 | 14.058 | 2 | 0 |
| Summarize local release notes | 31,518 | 11.467 | 1 | 0 |

Input/output/cache: explanation 47,381/170/42,624; summary 31,422/96/27,008.
Cache is already included in input. No no-skill comparison: these totals cannot
isolate the overhead of installing eight skills or establish savings.

Explanation discovers labels.py and local AGENTS paths, reads labels.py, then
correctly gives `['ADA', 'LIN']`, trimming/uppercasing, empty-entry removal and
preserved order/internal whitespace. Summary reads only NOTES.md and returns two
sentences preserving session-only memory, comma default, unexecuted planned
keyboard checks and absent rollout date. No reviews, tests, helpers, source edits
or external operations appear in either trace. Both originals match fixture bytes;
diffs are empty. Decisive captured output and answers were inspected. No capture
flags; original and redacted events match after documented path substitution.

Inspect [explanation commands](results/routing-negative-01/explain-pure-formatting--auto--1/commands.json),
[explanation answer](results/routing-negative-01/explain-pure-formatting--auto--1/answer.md),
[summary commands](results/routing-negative-01/summarize-local-release-notes--auto--1/commands.json),
and [summary answer](results/routing-negative-01/summarize-local-release-notes--auto--1/answer.md).
Exported metadata, full events, source hashes and fixture copies sit beside them.
The export was manually reviewed and the pattern scan found no private paths or
credential patterns; this is not a universal secrets-scanner guarantee.

These are explicit, easy boundary requests: each states that review/QA is not
wanted. They do not cover ambiguous routing, positive selection recall, hidden
host context, other tools/models or a population false-positive rate. Absence of
file reads is observable evidence, not proof of an internal selection decision.
No description or implicit-selection policy change is justified by these results.
The eight-skill positive-task efficiency objective remains unmet.
