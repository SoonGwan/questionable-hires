# Usage-first screen: shorter read adopted, total token cost still adverse

2026-09-14. [Protocol](HOSTAGE-JAVASCRIPT-USAGE-MODEL-01-PROTOCOL.md), launch
`8d21e74`, resource `f0b29dd`. [Evidence](results/hostage-javascript-usage-model-01/run.json).
One exposed authored task, fresh serial Astra medium baseline/skill, n=1 each.
Both complete, no timeout/exclusion/retry. No general efficiency claim.

| Observation | Baseline | Skill |
|---|---:|---:|
| Input + output tokens, cached input included | 87,491 | 114,460 |
| Process wall seconds | 92.970 | 86.698 |
| Output tokens | 2,674 | 2,277 |
| Completed shell calls | 5 | 6 |
| Captured native passes | 6/6 | 7/7 |
| New test file lines / bytes | 207 / 6,636 | 146 / 5,426 |
| Copied support lines / bytes | 0 / 0 | 165 / 6,362 |

Within this pair: **+30.82% total tokens / −6.75% wall time**. Counts differ because
baseline groups async/sync failure in one test. More test names are not better
coverage; fewer authored lines are not lower total code size with copied support.
Earlier pairs are historical context, not a controlled before/after comparison.

## Reviewed original behavior

Both implementations have identical per-instance pending/guard/await/finally
behavior and preserve both existing tests and requirements byte-for-byte.
Baseline authors observe/within/harness plus cleanup. It covers actual pending
entry, signal/result identity, two consecutive duplicates while save is pending,
independent instances, sync/async error identity and retry, actual abort-driven
callback rejection and retry with a fresh signal. Callbacks and tasks have
immediate rejection observation; finally releases/drains owned work and listeners.
Baseline also explicitly retries after ordinary success.

Skill batches application reads with the **42-line opening usage comment only**;
the original output ends at its closing delimiter. No full implementation read
appears. It copies the entire module exactly and uses withControlledCalls for
all five added tests, without rewriting lifecycle machinery. It covers required
state/identity/duplicate/independent/failure-retry/abort-retry behavior, with
listener removal in finally. It explicitly asserts synchronous callback failure
does not turn submit into a synchronous throw before registering the returned
Promise, preserving the header's caveat. Unlike baseline it does not add a
separate ordinary-success retry witness. Extra work differs.

Native output captures every test name and pass/fail/cancel/skip counts, with
test-specific exit 0. Native durations 48.387125ms baseline / 52.176875ms skill
are not model task time. Skill's empty mkdir/cp output is legitimate. Its batched
read ends exit 1 because the final AGENTS search has no matches; preceding reads
are captured. Final diff exits 1 for a new-file `git diff --no-index`, not failed
tests. No observed scope or test-capture exception. Skill prints the entire new
146-line regression file during final review; do not infer that all shorter-read
savings survive subsequent work or assign a causal fraction of cost to that read.

## Separate author replay

[Replay evidence](results/hostage-javascript-usage-model-01/author-replay.json)
reconciles original raw usage/sanitized events, frozen installed resources,
unchanged originals, copied module identity and exact reviewed inventories.
Original retained projects remain unchanged. Ten disposable-copy runs preserve
all retained tests/support, with 15-second outer process bounds:

| Implementation | Baseline pass/fail | Skill pass/fail |
|---|---:|---:|
| Final | 6/0 | 7/0 |
| Original | 2/4 | 2/5 |
| Missing guard | 5/1 | 6/1 |
| Missing cleanup | 2/4 | 2/5 |
| Wrong signal | 3/3 | 4/3 |

All expected outcomes match, no process timeout/cancel/skip. Skill's missing
guard is caught by the bounded application wait, not an outer process hang.
This replay does not replace original model evidence.

## Decision / next direction

Usage-first routing is behaviorally adopted; total cost reduction is unproven.
Do not market this as a gain or keep retuning the same exposed SubmitPanel task
until a favorable number appears. Preserve the usable helper/routing as a
development candidate and move to a different ownership/workflow contract before
further efficiency conclusions. The all-eight real-use objective remains open;
shared host/cache, n=1 and unequal extra work preclude broad causal claims.
