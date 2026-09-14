# Hostage controlled-call model screen 01

Candidate `d9e7711`; this protocol's commit is launch. Previous turn implemented
the optional asset and native controls, with 452 local tests passing. This is
progress, not model efficiency evidence.

Freeze the unchanged `necessary-state` case from bundle-contract-v2-cases.json,
SHA-256 `1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65`.
One author-exposed task, two fresh serial Astra medium sessions, baseline/skill,
n=1, seed 20260914, timeout 240s per cell. Retain every attempt; no favorable
retries/exclusions. Stop scheduling on account limits. No skill/task edits or
author test workloads during timing. Poll confirmed live handles on observation
loss; do not restart solely for a polling failure.

Review actual Form implementation and rerunnable native tests for initial/pending
state, duplicate suppression, independent instances, result/exception identity,
failure/retry and cancellation cleanup. Check bounded waits and owned-task cleanup,
original-file preservation outside requested edits, and no unrelated deployment.
Helper adoption is optional, not a scored obligation. Record asset/reference reads,
copying versus custom gates, test coverage and extra delivery work. A cheaper but
incomplete verification is not an accepted win.

After terminal completion export/reconcile raw usage/events and installed resource
bytes. Manually inspect implementation/test inventory; the read-only reconciler
is not valid for this implementation task. Independently replay retained tests
against original and corrected implementations with subprocess bounds; record
native intended failures and unchanged after passes without replacing original
model evidence. If new tests need stronger controls, disclose them separately.

N=1, exposure, shared host/cache and unequal work prevent causal/general savings
claims. Update EN/KO status/capability with limitations; preserve featured and
historical results. Native control evidence does not complete the all-eight goal.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/bundle-contract-v2-cases.json --case necessary-state --output benchmarks/local-runs/hostage-call-model-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 --timeout 240 --model gpt-6-astra --effort medium
```
