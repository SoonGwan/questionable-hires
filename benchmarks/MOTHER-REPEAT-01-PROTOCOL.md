# Frozen repeated-query native QA comparison

Candidate skills at `c6589ee`, including Mother-in-law's optional standalone
controlled transport asset. One new **authored synthetic** task, selected to
exercise repeated identical submissions and native-test delivery. It is not
organic production history, an independent holdout or all-eight acceptance.

Both arms get identical Search source, explicit newest-request requirements and
the initial native unittest. Source uses query equality as its completion guard;
it protects different queries but misses stale responses for identical queries.
Models must retain ordinary failing regressions for discovered bugs, not fix
production, change expectations, skip or mark expectedFailure. Required same-key
and different-key sequences include seeded complete payloads and all intermediate
checkpoints, actual fetch keys, bounded waits and failure-safe owned-task cleanup.
Standalone standard-library support may be added but no installed-skill runtime
dependency or separate report is wanted. No helper adoption is itself scored.

Author fixture preflight: **3 tests pass (0.016s)**. Original same-key reverse
completion fails on actual old versus expected new structured payload, not support
errors. Different-key reverse completion passes. A separate author-only request
identity counterfactual passes both sequences. Witnesses use real Search, actual
fetch entry, independent per-request Futures and cancel/join owned tasks in finally;
no filesystem scratch, network or sleeps. Witnesses/counterfactual are excluded
from model input. The new support asset separately has a deliberate wrong-key
AssertionError regression with actual/expected values, not a TestCase.fail wrapper.

Run two fresh serial Astra medium sessions, baseline and skill once, fixed seed
20260913, 240-second caps. Freeze all files before scheduling. No model retries,
exclusions, candidate/fixture edits or concurrent author tests during timing.
Stop scheduling on account limits; preserve every scheduled result and capture
limitation. Review native assertions/controls, standalone retained files, scope,
cleanup and resource integrity before comparing input (cached once) + output and
wall time. Shared host/cache, n=1, selection and unequal work limit attribution.
Keep historical/featured graph numbers unchanged.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/mother-repeat-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260913 --timeout 240 \
  --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/mother-repeat-01
```
