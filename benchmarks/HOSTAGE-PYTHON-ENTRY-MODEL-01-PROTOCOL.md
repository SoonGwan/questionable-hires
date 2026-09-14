# Python task-aware callback: adoption screen 01

2026-09-14, resources `4b79eb9` (Python asset introduced at `6d57e68`).
One fresh explicit-skill Astra medium session, one job, seed 20260911,
240-second bound, no favorable retry. Use only `necessary-state` from the
unchanged exposed `bundle-contract-v2-cases.json`, SHA-256
`1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65`.
Do not give the model prior answers, faults or this review protocol.

This is an adoption/correctness check, not a paired performance experiment.
The optional Python `started_before` API is locally tested but model adoption
is unmeasured. Record whether the generated tests use it with the corresponding
owned application task; non-adoption is a result, not grounds for another run.
Record absolute token/time cost and all initial errors or capture gaps. Historical
checkpoint 07 has unequal test work and is not a causal efficiency comparator.
No source edits or author test workloads during model timing.

Before launch run the native controlled-call asset tests, including correct
two-stage identity preservation and skipped-decode negative control. The task
and criteria remain frozen; do not add requirements just to trigger the API.

Review pending transitions, duplicates, separate instances, exact return/error
identity, synchronous failure, retry and cancellation cleanup against the actual
task. Separate supplementary coverage from mandatory requirements. Reconcile raw
usage, installed/copy hashes and original project files. Retain all generated
tests. Separately replay unchanged tests against final/original code and narrow
missing-guard/missing-cleanup faults, adapting only the production transformation
to the generated implementation. Bound replay processes and retain native counts
and intended failure details; these cannot replace missing original evidence.
No featured chart or historical score changes.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/bundle-contract-v2-cases.json --case necessary-state --output benchmarks/local-runs/hostage-python-entry-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
