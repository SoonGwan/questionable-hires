# SQLite commit audit transfer 01 — 2026-09-14

Resources `8e3bdc4` (same skill files at prelaunch `64f79ae`). Two fresh serial
Astra medium sessions, baseline/explicit skill, n=1 each, seed 20260911, 240-second
bound per cell. One new authored task, not an independent real-project holdout.
The case JSON and its digest are frozen in the launch commit/run manifest before
either model starts. No favorable retries or task/resource edits during timing.

This transfers from a two-file list append to a disk-SQLite commit through an
imported endpoint/writer alias. Native receipt tests accept acknowledgments but
do not inspect durable rows. Required obligations are explicitly model-visible:
read actual sources, verify test/endpoint/writer bindings in the check process,
run correct and missing-commit existing tests, verify the same stronger native
row assertion on both through a fresh connection, preserve old and binary rows,
preserve originals and remove project-local scratch. Audit only, not a repair.
The model gets task/project files, not the author stronger probe or expected answer.

Preflight uses real SQLite databases and both actual native receipt tests plus
one stronger native test. Correct tests/probe pass; missing-commit original tests
still pass, stronger probe fails with the intended missing binary row AssertionError.
The old row remains. Same-process binding assertions pass; all test scratch uses
the copied project and is removed. Original files stay unchanged. The generator
and regression test retain these controls; no happy-path-only preflight.

Review recorded reads/reference adoption, actual native outputs/counts, binding
and file provenance, intended failures versus setup errors, and extra work. A
valid native/project audit need not adopt the optional helper. No source/guide
read may mean absent or missing evidence; neither infer adoption nor silently
credit source inspection. A surviving fault does not prove all test quality.

After timing, reconcile raw usage/events, frozen resource bytes/modes and complete
retained inventories. Author replay is separate, cannot fill original gaps and
must preserve each model's actual tests/recipes. Retain timeout/unattempted/unknown
usage and errors; don't substitute zero for unknowns. Compare full-session tokens
and wall time only with these limitations: n=1/shared host/cache/unequal work,
new but author-selected task, not causal guide improvement or all-eight superiority.
No featured/historical chart changes. Update dated EN/KO status after review.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/con-artist-sqlite-cases.json --output benchmarks/local-runs/con-artist-sqlite-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
