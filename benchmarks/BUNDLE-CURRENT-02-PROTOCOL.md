# Current bundle regression 02: frozen exposed gate

Use unchanged `fast-cases.json`: nine tasks covering all eight skills. One fresh
baseline and one explicit corresponding-skill session per task, 18 total. All
skill resources are frozen at `e02c9bb`; this protocol is committed before running.
No automatic-selection or control arm; this gate cannot establish routing recall.

Astra medium, repeats=1, jobs=1 (serial), seed=20260911, 240-second session limits.
Use the current `run.py` without edits. Keep the recorded shuffled schedule,
fixture hash, entrypoint hashes and per-cell resource inventories. Stop scheduling
after a recognized account limit. No retries, exclusions, fixture/criteria changes
or candidate changes during the run. This run consumes model usage.

This is the same exposed regression set as bundle 01, not held-out confirmation
or an optimization target. It checks accumulated changes, including updated
Landlord discovery and Con Artist same-process provenance/reuse guidance. It does
not prove causality for any individual change or require optional-helper adoption.

Review all original commands/output and final files against the existing case
criteria. Record missing output, failed patch scope uncertainty, unrun checks,
extra work and unequal coverage. Never reconstruct missing execution from final
prose or credit author replay as model behavior. Completion is not correctness.

Report per-pair input plus output tokens (cached input already included), wall
time and observed outcomes, retaining adverse samples. A shared-host single-repeat
gate is descriptive, not broad superiority or proof of the user's requested
substantial improvement. Do not repeat this unchanged gate to obtain better scores.

Command from repository root:

```sh
python3 benchmarks/run.py --cases-file benchmarks/fast-cases.json \
  --output benchmarks/local-runs/bundle-current-02 --arms baseline skill \
  --repeats 1 --jobs 1 --seed 20260911 --timeout 240
```
