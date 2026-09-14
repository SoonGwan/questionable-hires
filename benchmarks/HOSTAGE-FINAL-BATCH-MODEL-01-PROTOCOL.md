# Final batching and dependent-phase adoption — screen 01

2026-09-14, resources `fc557ad`. One fresh explicit-skill Astra medium session,
one job, seed 20260911, 240-second process bound; no favorable retry. Unchanged
exposed keyed-import task, SHA-256
`b3e35518b205ffb535c15bec6b03ccfe896c2af70094cf41c79fd27918e29880`.
Do not provide previous answers, faults, author adaptations or this protocol.

Since keyed-import 01, only Python dependent-phase guidance and final-check
batching guidance changed in the skill. Native candidate preflight has 502
repository tests passing, including actual final-check success/failure controls,
independent versus dependent subtests, and callback execution. Fixtures are frozen.
No skill/task edits or author test workloads during model timing.

Review every original task obligation, actual tests and copy integrity, not just
shell counts. Specifically record whether native tests, copy checks and final
diff/status share a failure-preserving call; do not require redundant checks or
claim a failure for justified intervening decisions. Inspect dependent async
phases and cleanup after a prerequisite failure. Preserve original errors, gaps,
unknown usage, extra work and all resource hashes. A full-source reread still counts.

Separately replay retained tests unchanged against final/original code, valid
alternate duplicate results and missing guard/cleanup/all-key-blocking faults.
Adapt production transformations only to the actual generated implementation;
bound each replay at 20 seconds and inspect intended versus secondary errors.
Do not rewrite model tests or replace missing original output with author replay.

Report absolute tokens/time and observed adoption. Earlier keyed-import 01 used
118,971 tokens / 103.161s; any descriptive difference has n=1, shared host/cache,
different generated verification and two simultaneous instruction changes. It
cannot isolate causality or establish a general gain. No featured chart update.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-keyed-import-cases.json --output benchmarks/local-runs/hostage-final-batch-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
