# Hostage keyed publication — transfer screen protocol

Candidate skill and collector `7dd4b56`; callback asset `d9e7711`. Launch from
this committed protocol and record exact HEAD in run.json. No model run yet.

New author-written development case in hostage-keyed-publish-cases.json, SHA-256
`06d3940100bf82fe8f00a55b38ed318118854e34778e1615f55297915f9f8702`.
This is a transfer probe from global Form.pending to same-document/same-instance
suppression with cross-key concurrency, not independent holdout or organic use.
The visible contract explicitly preserves callback signature/object identities,
caller-driven retry, synchronous/async failure and cancellation cleanup, existing
tests, bounded new regressions and accurate execution reporting. No helper is
mandated and no author correction/control code is provided to the model.

Native preflight: three author tests pass in 0.454s. The supplied two-test runner
passes original source and exposes deliberate `doc != wrong` assertion failure.
Correct keyed-state control passes existing tests and concurrency/recovery probe.
Original source fails with observed duplicate calls 2 versus expected 1; a global
busy control fails because another document is suppressed. All subprocesses have
10-second bounds, async waits/cleanup are bounded, no extra project files remain.
These are harness controls, not model outcomes or full application acceptance.

Schedule only this one case: two fresh serial Astra medium sessions, baseline
and skill, n=1, seed 20260914, 240 seconds/cell. No favorable retries/exclusions;
retain incomplete usage as unknown. Stop new scheduling on account limits. No
resource/fixture changes or author test workloads during timing. Poll live handles
on observation gaps; never restart solely for missing polling output.

After completion review actual callback bindings, keyed/instance ownership,
all explicit transitions and unchanged original tests. Inspect native count/results
and test-specific status, not final shell success. Export every attempt, reconcile
raw usage/resources/inventory and independently replay retained tests against
original/final and relevant incorrect-state controls under subprocess bounds.
Keep replay separate from original output and preserve any evidence gaps.
No broad/causal efficiency claim from one exposed pair, shared host/cache or
unequal work. Update EN/KO capability/status after review; keep featured fixed.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-keyed-publish-cases.json --output benchmarks/local-runs/hostage-keyed-publish-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 --timeout 240 --model gpt-6-astra --effort medium
```
