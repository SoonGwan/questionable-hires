# Improve first, then measure a small fixed set

The owner requested all-skill improvement with fewer than ten tasks per development set. The long HTTPX comparison was stopped on request; completed evidence remains under ignored `local-runs/httpx-2026-09-11`. Its missing cells are unattempted/interrupted, not successes, failures, or a completed comparison. The in-flight cell may lack captured stdout because the runner was terminated; its workspace was preserved.

`fast-cases.json` contains nine existing regression tasks: one for every hire plus a protected-interaction negative control. The trivial label change is replaced by necessary pending-state behavior, testing that scope discipline does not omit required work. Cases and criteria come from existing main/clean suites; these are exposed development regressions, not held-out evidence or proof of broad superiority.

## Development loop

1. Inspect the actual failure or wasteful behavior; revise the skill's decision process before running more models.
2. Run local validation and tool tests. Check only changed hires first, one independent sample each. Use baseline/previous-snapshot comparisons on those same tasks when evaluating efficiency; start with at most five paired tasks (ten executions), not a full repeated matrix.
3. Inspect artifacts and record correctness, scope, meaningful evidence, token usage, wall time and failure cause. Do not reward skipped requirements, shorter prose, or fewer lines alone.
4. Revise the demonstrated weakness and repeat. Before accepting an iteration, run the nine-task skill-only regression screen once; ties are not improvement, and a single successful sample is not reliability proof.
5. Freeze a candidate before a small separate confirmation set. Do not tune on its answers or advertise development scores as held-out results. Expand only when evidence or the owner justifies the time.

```sh
python3 benchmarks/run.py --cases-file benchmarks/fast-cases.json --case persistence-test --arms baseline skill --repeats 1 --jobs 1 --output benchmarks/local-runs/fast-con-artist-01
python3 benchmarks/run.py --cases-file benchmarks/fast-cases.json --arms skill --repeats 1 --jobs 1 --output benchmarks/local-runs/fast-regression-01
```

Use new output directories, retain adverse runs, and compare identical model/effort/environment. Lower token/time at preserved task outcomes is the efficiency target; unchanged cost with stronger outcomes is also useful. Higher cost needs a demonstrated benefit and explicit tradeoff, not a performance claim. Do not hide results or change criteria to manufacture a win.

## All-skill candidate changes

- Necromancer: connect historical constraint to present necessity; stop once a live counterexample settles removal.
- Receipt: reuse a stable regression before/after; preserve real command exit status and test only affected contracts.
- Landlord: compare actual future maintenance steps and obligations rather than counting abstractions or lines.
- Mother-in-law: select a short state-crossing sequence and nearest control; assert the effect at the layer that owns it.
- Exorcist: observe the boundary where causes diverge; select only decision-changing experiments.
- Hostage Negotiator: trace supporting edits to acceptance conditions; distinguish required state from optional redesign.
- Con Artist: test lifecycle/effect boundaries, verify mutated imports, and distinguish one killed fault from all coverage.
- Friday: walk actual rollout and rollback states, including newly written data and the last recoverable point.

Repeated generic instructions were compressed while retaining user scope and evidence boundaries. These revisions are candidates until behaviorally checked; shorter text alone is not measured performance improvement.
