# Display-retention model checkpoint 01

Three new authored development cases: guarded behavior, clearing on request entry,
and transient stale display repaired by the latest completion. Not organic tasks,
not independent holdouts and not a representative all-eight result. The tasks
exercise the capability just implemented; that selection bias remains explicit.

Freeze `retention-cases.json`, SHA-256
`7f0f99da367c18ba1e67f45e18ea9c79bb1d406cea3a84221bca67c1368bff36`.
The model-visible contract requires retaining the displayed result until the
latest succeeds, at request entry and at intermediate/final completion. Actual
Suggestions.search/last_result differs from helper defaults. No project-regression
deliverable is required; captured observations and a rerunnable command are.
Source preservation, bounded waits and owned-task cleanup are explicit.

Preflight: two fixture tests pass (0.027s), invoking actual compiled fixture code
through native async operations with nondefault query values. Guard passes;
clear fails with actual null/expected seeded payload; transient fails with actual
older/expected seeded payload even though final latest display is correct.
Nineteen helper tests pass (0.632s), including preserved transient evidence and
owned-task cleanup on timeout. These are author tests, not new model evidence.

Prospective schedule: six fresh serial Astra medium sessions, baseline and explicit
skill for each case, one repeat, seed 20260914, 240-second cell limits. No task or
resource edits or author test workloads during timing. Keep every scheduled cell,
timeout, missing output, extra artifact and scope deviation. Do not retry or
exclude cells for preferred numbers; stop scheduling on recognized account limits.

Review exact asserted states, actual component bindings, both orders and original
preservation. Helper invocation alone is not success. Report missed transient
faults and false positives separately; final state alone cannot establish success.
Count input plus output, cached input once; unknown usage remains unknown. Report
all elapsed time but do not compare timeout-to-completed ratios as task speed.
Unequal extra sequential/helper checks must remain disclosed. No featured-chart
promotion or all-eight/20–30% gain based on this single-repeat targeted comparison.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/retention-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 \
  --timeout 240 --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/mother-retention-model-01
```
