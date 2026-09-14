# Dependent async phases — remove misleading follow-on errors

Subsequent [model adoption screen](HOSTAGE-FINAL-BATCH-MODEL-01-REVIEW.md)
generates sequential dependent phases without the prior secondary errors in
separate fault replays. Its capture/cost limits are distinct from this author control.

2026-09-14, author control on frozen keyed-import artifacts at `e8ab180`.
[Original model review](HOSTAGE-KEYED-IMPORT-01-REVIEW.md);
[all twelve native outputs and adapted source](results/hostage-dependent-phases-01/author-control.json).
This is a local test-structure correction, not a fresh model or performance result.

The original generated tests put fetch and persist phases of the same live call
inside separate `unittest.subTest` contexts. A failed prerequisite is recorded
and execution continues. Later code then references `saved`, which the failed
phase never assigned. Missing guard, missing cleanup and all-key blocking each
produce this secondary `UnboundLocalError` alongside the real failure.

The Python callback asset's usage docstring now distinguishes independent
scenarios from dependent phases: the latter must unwind to owned cleanup after
a prerequisite failure. This runtime-specific guidance remains in the optional
asset rather than adding requirements to every Hostage task. No executable asset
code, public API or historical generated artifact changes.

## Native evidence

The author adaptation removes only two dependent-phase subtest wrappers from
copies of the retained tests. It preserves every assertion, application call,
await and cleanup expression. Independent scenarios still use their existing
subtests. Two local regression tests exercise native behavior and check that only
the intended wrappers change; they work from tracked evidence without Git history.

Both original and adapted test sources are run against the same six production
variants, in disposable project-local directories under 20-second process bounds.
All twelve discover six tests. Final code and valid False-returning duplicates
pass in both modes. Original missing state, missing guard, missing cleanup and
all-key blocking still fail. The three previously noisy fault variants no longer
include `UnboundLocalError`; intended callback/state/entry failures remain.
No run times out. Original retained artifacts are read from Git, not rewritten.

| Fault | Original captured characters | Adapted captured characters |
| --- | ---: | ---: |
| Missing duplicate guard | 3,465 | 2,463 |
| Missing cleanup | 7,683 | 6,604 |
| Blocks other keys | 6,741 | 5,662 |

These are lengths of full normalized native transcripts, not tokens, processing
time, or independent defects found. Path normalization is identical across modes.
Fewer failures inside a dependent scenario is expected: the test now stops at
the first broken prerequisite. Other independent scenarios continue. This does
not prove all future fault diagnostics are clean or that every individual
assertion kills every fault.

The author deliberately applies the guidance to old tests; it does **not** show
that a new model will follow it. That adoption and whole-task cost remain
unmeasured. The entry docstring grows slightly. No general 20–30% claim, featured
update, favorable retry or deletion of adverse model output is justified.
Validation: executable Python AST unchanged; native callback tests 16/16 pass;
full repository suite 501 tests passes in 70.688s without failures/skips. Catalog,
skill validation and featured EN/KO synchronization checks pass.

Reproduce the separate author control (new output path required):

```sh
python3 -B benchmarks/probe_hostage_dependent_phases.py --scratch-root benchmarks/local-runs --output benchmarks/local-runs/dependent-phases-new.json
```
