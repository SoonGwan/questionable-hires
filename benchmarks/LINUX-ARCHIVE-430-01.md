# Current source-archive check — 2026-09-14

Network-disabled Linux arm64/Python 3.12.3, using the existing image
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
Host archive and existing PyYAML 6.0.3 package are mounted read-only. PyYAML runs
without its compiled extension. No download or dependency installation occurs.
The container copies the archive to its own writable directory, verifies `.git`
and `benchmarks/local-runs` are absent, then validates catalog/localized charts
and runs the full suite. Each container uses `--rm`; host archives are retained
under ignored local runs. This is not fresh-install or hosted-CI evidence.

## Initial result at `cc7ac4d`

430 discovered, **one failure and two skips**, 60.956s. The failure is
`test_retention_timeout_cleans_owned_overlapping_tasks`. The two skips are the
existing Git-provenance comparisons, not native packaging regressions. Archive:
`benchmarks/local-runs/linux-cc7ac4d.8ithRo`.

An isolated diagnostic preserves the original failing test and records identity:
the three entries are `(is current unittest task, done)` =
`(True, False), (False, True), (False, True)`. Both owned peers are already done;
the seed ran in the current unittest task, which cannot be done while asserting.
This disproves the test's task-ownership assumption on this runtime, not the
helper's actual peer cleanup. The isolated check fails again in 0.058s.

## Narrow test correction `a81692f`

Explicitly create the sequence task before passing it to wait_for. Preserve the
50 ms timeout, all three finalizer checks and done assertions, and additionally
assert seed identity and exclusion of the still-running unittest task. Runtime
skill code and measured benchmarks are unchanged. macOS/Python 3.9.6: all 19
sequence-probe tests pass in 0.647s.

An unmodified archive of the corrected commit is rerun through the same Linux
pipeline, not overlaid onto the failed archive. Location:
`benchmarks/local-runs/linux-a81692f.yta5ax`. Result: **430 discovered, 428 passed,
two explicit Git-provenance skips, 60.274s**, exit 0. Catalog, localized featured
charts and full suite pass without code overlays. Native all-eight installation
and the three recent inherited-pipe regressions are included.

These platform checks do not establish model-token efficiency or general
developer-task gains. Original failing evidence is retained, not rewritten.
