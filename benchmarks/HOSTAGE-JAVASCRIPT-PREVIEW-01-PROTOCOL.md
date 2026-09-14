# Two-stage PreviewLoader transfer screen

2026-09-14. Resource candidate: `f0b29dd` (usage-first JS route, unchanged runtime
from `22bd929`). New task: `hostage-javascript-preview-cases.json`, SHA-256
`fd9d98e8557845c3f25aff22f7576c850323f7c0a815528427f7c486338f8c5c`.
This is an author-designed transfer task, not an independent holdout or a real
user repository. Do not relabel the earlier exposed SubmitPanel experiments.

## Contract fixed before model timing

One existing ES-module PreviewLoader, two original native tests and explicit
requirements. Implement latest-invocation state ownership across fetch/decode,
including same-key requests, stale success/failure while the newest call is
loading/ready/failed, prior displayed-value preservation, per-instance isolation,
both-phase key/bytes/signal/result/error identity and sync/async failure recovery.
Stale callers still run decode after successful fetch and retain their own result
or rejection. Cancellation remains callback-owned; test real abort rejection.
Retain native regressions, original tests unchanged, bounded waits and cleanup.
No dependencies, services, delegation, browser work, other skills or publishing.

The helper is not injected into baseline. Reference implementation and contract
tests under `tests/` are author-only and do not enter either model workspace.

## Author preflight

`tests/test_javascript_preview_fixture.py` runs native Node in project-local
temporary directories, with 15-second subprocess deadlines. Original and
corrected owners both pass the two supplied tests unchanged. The corrected
owner passes all 18 tests including 16 author-only tests: 12 overlap combinations
(old fetch/decode × old success/failure × newest loading/ready/error), initial
state/value preservation/recovery, sync/async errors in both phases, isolation,
and actual decode-stage signal-driven rejection with retry.

Seven deliberate native faults all fail with AssertionError actual/expected
evidence, with all 18 tests discovered, no cancellation/skip or contract timeout:
unguarded stale success, unguarded stale error, reused generation, wrong decode
signal, lost displayed value, global ownership across instances, and skipping a
stale decode. Original test sources and requirements remain unchanged in copies.
Three Python preflight tests passed in 0.892s before the additional discovery
assertion. These are fixture checks, not model performance measurements.
Full local preflight afterward: 473 tests passed in 64.942s, no failures/skips.
Repository validation, featured-language sync and diff checks passed.

Pre-freeze authoring corrections are disclosed: the first draft used structural
equality for empty result objects and missed a stale-value fault; explicit
reference equality now detects it. A callback assertion before an entry marker
initially became an entry timeout; waiting for entry **or actual task failure**
now preserves its native AssertionError. No model cell was run on those drafts.

## Schedule and review

After full local validation, freeze the launch revision. Two fresh serial Astra
medium cells, baseline and explicit skill, n=1 each, seed 20260911, jobs 1,
240 seconds per cell. Preserve every attempt, timeout, unknown, scope violation
and capture gap; no favorable retries or exclusions. Do not edit task/resources
or run author tests during timing.

Review actual state ownership and all explicit regression obligations, not just
test counts or final prose. Inspect usage-comment reads, helper copy/adoption,
scope, original native verification exits/output, unchanged original tests and
extra work. Reconcile raw usage and frozen resource hashes; replay retained tests
without changing their sources on original/final and reviewed native faults in
separate bounded copies. Replay does not fill original output gaps. Report costs
even if adverse. No featured promotion or general claim from one authored pair.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-javascript-preview-cases.json --output benchmarks/local-runs/hostage-javascript-preview-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
