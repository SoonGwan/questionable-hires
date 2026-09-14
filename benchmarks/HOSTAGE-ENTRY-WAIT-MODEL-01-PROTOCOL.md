# Task-aware entry: fresh model adoption screen

Resource `328bc1f`. One fresh explicit-skill Astra medium session, jobs 1,
seed 20260911, 240-second limit, no favorable retry. Unchanged exposed task
`hostage-javascript-preview-cases.json`, SHA-256
`fd9d98e8557845c3f25aff22f7576c850323f7c0a815528427f7c486338f8c5c`.
Do not pass earlier model answers, author adaptations or faults to the session.
No resource/task edits or author test workloads during timing.

The [native candidate](HOSTAGE-ENTRY-WAIT-01.md) has 483 local tests passing,
including positive/negative two-stage entry controls and a retained-test author
adaptation. This fresh screen tests whether a model independently uses the new
optional API with the correct task while preserving application assertions.
This is not a baseline comparison or general efficiency experiment; report
absolute cost, including any timeout/unknown usage and initial failed tests.

Review all original task obligations: latest-only state across both phases,
same-key ownership, return/error/argument identities, state contents, recovery,
instance isolation, callback-owned abort, bounded waits and owned cleanup.
Check whether startedBefore is used, whether it observes the corresponding task,
and whether it replaces application assertions improperly. Record full-module
reads, copy verification, extra work, scope exceptions and capture gaps.

Reconcile raw usage/events, unchanged installed resources, copied asset, exact
project inventory and preserved original tests/requirements. In separate copies,
run retained tests unchanged against final/original code, valid mutable updates,
stale in-place success/error and skipped-stale-decode code. Include the existing
additional fault controls when their transformations match the actual code.
Preserve all output and process bounds. For skipped decode, distinguish early
entry failure from deadline-only failure; replays are not model evidence and
cannot repair missing original output. Do not compare unequal model test suites
as if identical work. No featured graph or historical score changes.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-javascript-preview-cases.json --output benchmarks/local-runs/hostage-entry-wait-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
