# Linux source archive after recent helper changes — 2026-09-14

Local Linux arm64, Python 3.12.3, Node v24.20.0, existing PyYAML 6.0.3 in
pure-Python mode. Existing image
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
Networking disabled; source archive and existing PyYAML mounted read-only. The
container copies source to its writable `/work`, confirms no `.git` or ignored
`benchmarks/local-runs`, validates catalog/localization and runs the whole suite.
No downloads, code overlays or model sessions. Containers use `--rm`; host
archives remain in ignored local runs.

## Initial unmodified archive `7087e52`

[Full log](results/linux-archive-497-01/initial-7087e52.txt): 496 discovered,
one error and two skips, 27.999s, exit 1. Friday's frozen comparison test calls
`git ls-tree b2816cd` without checking whether the archive includes history.
The failure is unavailable historical provenance, not a failed skill runtime
or SQL check. Archive: `benchmarks/local-runs/linux-7087e52.utVhKT`.

## Corrected unmodified archive `57d48fd`

The historical resource comparison first checks both pinned commits and skips
explicitly if unavailable. Schedule settings, terminal failure handling and
no-retry checks still execute. A separate temporary-archive integration runs all
three schedule tests with exactly one provenance skip. The normal checkout CI
job now requests full history so these comparisons can execute there; the source
archive job retains its intentional no-history environment.

macOS preflight: three Friday schedule tests pass with actual history (0.198s),
and three archive integration tests pass (1.371s). No runtime skill edits.

[Full corrected log](results/linux-archive-497-01/corrected-57d48fd.txt):
**497 discovered, 494 passed, three explicit Git-provenance skips, 28.060s**,
exit 0. Catalog, featured/localized-chart checks and native regression suite pass.
Skipped comparisons: packaging source provenance, packaging review provenance,
and Friday's historical compact-version snapshots. Their available native
behavior/schedule checks run. Archive:
`benchmarks/local-runs/linux-57d48fd.xQgAMl`.

This includes the latest Python/JavaScript task-aware callback waits, Friday
reader-snapshot reuse, physical source-line corrections and Node capture-warning
checks. It is not hosted CI, fresh dependency installation, a Python-version
matrix, remote host registration or model-performance evidence.

## Read-only hosted gate check

At the time of inspection, repository visibility remains private. Hosted
[run 34821858042](https://github.com/SoonGwan/questionable-hires/actions/runs/34821858042)
for `7087e52` has four failed jobs, each with **zero executed steps**. The source
archive annotation (`103905002027`) reports failed recent payments **or** a
spending-limit issue; it does not identify which account setting applies. This
does not establish a hosted test failure or verify the new full-history setting.
No billing, visibility, release, package publication or workflow rerun was made.
