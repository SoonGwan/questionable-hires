# Combined candidate: efficiency gate not met

Snapshot `9683528`, unchanged nine-task development set, GPT-6 Astra medium,
serial, one fresh skill session per case. All nine completed, with no retry,
exclusion or timeout. Source instruction hashes match every cell. All current
non-cache skill resource bytes were also compared with each retained installed
copy after the run; no mismatches. No skill files changed during execution.

| Case | Task criteria | Total tokens | Seconds |
| --- | --- | ---: | ---: |
| history-active | Pass | 69,328 | 28.584 |
| boundary-fix | Pass | 101,319 | 37.221 |
| formatter-review | Pass | 83,254 | 32.579 |
| search-order | Pass; scope violation | 87,163 | 73.232 |
| search-diagnosis | Pass | 67,869 | 41.228 |
| necessary-state | Pass | 87,385 | 76.587 |
| persistence-test | Pass | 87,055 | 32.540 |
| rolling-schema | Pass | 83,409 | 42.077 |
| search-protected | Pass | 66,993 | 39.649 |

Totals: **733,775 tokens**, input including cached input plus output, and
**403.697 seconds** summed process time. Relative to FAST-REGRESSION-02:
**+5.9% tokens, +14.3% time**. These separated single screens are descriptive,
not a paired causal effect estimate. Neither has a contemporaneous baseline.
The current collection does not meet the overall efficiency objective.

All answers, command traces and diffs were inspected against the original
criteria. Original fixture files changed only for the eligibility fix/tests
and Form implementation. Search QA/diagnosis added local reproductions; Form
added a regression suite covering cancellation as well as required transitions.
This is more retained verification than the previous Form sample, not an equal
effort comparison. The audit helper supplied correct/mutated test and probe
results with copied imports verified. History used native Git, not the optional
collector. Release review executed local old/new reader/schema combinations
and preserved a representative post-migration row through reversal.

Independent post-run replay of boundary, Form, protected search, faulty search
and diagnosis artifacts reproduced their expected outcomes. Faulty search
correctly reports one assertion failure, not an execution setup error. The
other four cases were checked from recorded traces and artifacts, not separately
replayed here. Combined shell commands were not scored solely by final exit.

Scope violation: search-order executed `find .. -name AGENTS.md -print` despite
the explicit project boundary. Thus task-specific criteria are 9/9, but the
collection is **not fully compliant** and must not be advertised as 9/9 overall
success. No comparable external search was observed in the other eight command
traces; this is a trace review, not a security sandbox certification.

Evidence remains under ignored `local-runs/fast-regression-03`. The screen is
now complete; do not rerun the unchanged candidate hoping for better numbers.
Next work must address demonstrated scope/cost causes or representative work,
not substitute individual favorable outcomes for this adverse aggregate.
