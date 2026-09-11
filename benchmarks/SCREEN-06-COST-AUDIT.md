# Screen 06 cost increase: observed differences, not a single cause

Read-only comparison of original event streams and metadata from screens 05/06.
No new model sessions, exclusions, changed scoring or skill edits. These are the
three largest absolute token increases; other tasks remain in the full totals.

| Case | Tokens 05 → 06 | Shell calls 05 → 06 | Uncached input 05 → 06 | Output 05 → 06 |
| --- | ---: | ---: | ---: | ---: |
| search-diagnosis | 68,288 → 86,896 | 3 → 5 | 11,030 → 7,990 | 1,066 → 1,338 |
| necessary-state | 68,289 → 86,872 | 4 → 3 | 7,037 → 7,926 | 1,220 → 2,018 |
| rolling-schema | 70,057 → 86,835 | 4 → 5 | 13,899 → 13,074 | 862 → 929 |

Tokens retain the original definition: all input, including cached input, plus
output. Uncached input here is input minus the separately reported cached subset;
it is diagnostic, not a replacement objective, bill estimate or superiority metric.

## What actually differs

- Diagnosis separates discovery/status from two already-known source reads, then
  separates execution from final diff/status. Output is larger and the retained
  probe adds bounded waits. More interaction rounds are a plausible overhead
  contributor, but new uncached input actually falls. No per-round usage accounting
  exists in these records to attribute exact costs to a particular command.
- Pending-state implementation uses the exact same skill SHA in both screens.
  Screen 06 has fewer shell calls, but one rejected patch and more generated output.
  The rejection does not identify its target. Do not invent a path-alias cause or
  attribute its entire increase to either the skill or the rejection.
- SQL review separates project inspection from reference/line-number inspection,
  adding a round. Both runs use the matrix and inserted-row rollback check. Both
  return four phase results; generated evidence does not show a new production
  verification capability. The entrypoint changed, but surrounding execution did
  too, so their isolated effects are unknown.

## Decision

Reject a blanket 'fewer calls means cheaper' explanation: the unchanged pending
skill is a counterexample in this screen. Also reject treating lower uncached input
as achieving the user's total-token goal. Keep all adverse totals unchanged.

A useful next candidate must remove a demonstrated repeated action while keeping
the same contract checks, and be evaluated on both a task that benefits and a
task where it should do nothing. Do not add a generic batching checklist to every
skill or accumulate more rules based solely on these separated samples. Existing
scope and cancellation gaps still require their own evidence; they are not cured
by fewer commands. Current overall performance remains unproven.
