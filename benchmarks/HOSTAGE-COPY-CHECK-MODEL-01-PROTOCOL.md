# Copy-check instruction: fresh adoption screen

Resource `ee1fa12`, unchanged runtime. Use the unchanged exposed
`hostage-javascript-preview-cases.json` (SHA-256
`fd9d98e8557845c3f25aff22f7576c850323f7c0a815528427f7c486338f8c5c`).
One new skill-only Astra medium session, seed 20260911, jobs 1, timeout 240s.
No favorable retry, prior answer, author test or hint beyond the frozen task and
installed skill. This is an author-designed adoption screen, not an efficiency
comparison. Report absolute cost; no baseline or historical causal percentage.

Preflight: affected copy/JS integration tests pass 4/4, including 17 native
behavior/lifecycle checks and identical/changed/missing copy controls. Full suite
at parent `6806512` passed 481 tests. Repository/skill/link/localization checks
passed for the instruction candidate. Keep fixture and resource unchanged during
timing; no concurrent author test or edit workloads.

Review original commands and outputs for header reading, copy verification and
whole-module reprinting. A bare `cmp` followed by another successful command does
not establish its own exit; inspect actual shell control flow. Copy equality
does not prove application correctness. Preserve all initial failures, unknown
usage, capture gaps, scope exceptions and scheduled outcomes.

Review retained implementation/tests against every explicit task obligation,
including state-content snapshots, identity, both-phase stale execution, actual
abort rejection, bounded waits and cleanup. Reconcile original files, inventory,
installed resource hashes and raw usage. Separately replay native tests against
final/original implementations, valid guarded mutable publication and unguarded
in-place success/error. Preserve actual failure output and deadlines; replays
cannot fill missing original evidence. Document extra work and uncovered cases.

No featured chart change or broad 20–30% claim follows this one session. Update
dated candidate status and both README languages with reviewed findings.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-javascript-preview-cases.json --output benchmarks/local-runs/hostage-copy-check-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
