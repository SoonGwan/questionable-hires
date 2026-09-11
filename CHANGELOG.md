# Changelog

## Unreleased

- Failed local package builds now attempt to remove their newly created output,
  allowing retry after successful cleanup. Existing destinations are never
  eligible for cleanup. The original error or cancellation is preserved even
  when cleanup itself fails; in that case partial output can remain.
- Added regression coverage for late-copy failures, cancellation, retry,
  cleanup failure and existing file/directory/symlink preservation. The full
  local suite passes 183 tests; this is not hosted-CI or model-performance proof.

## 0.1.0 — development preview

- Added eight focused developer skills with UI metadata.
- Added a local installer that refuses overwrites and rolls back failed copies.
- Added Codex plugin metadata and automated catalog/installer checks.
- Added deterministic engineering fixtures and a three-arm Astra evaluation runner.
- Added installation instructions, evaluation criteria, and contribution templates.
- Recorded three-arm Astra smoke comparisons, clean cases, and full-team automatic routing.
- Published eight worked examples with actual commands, diffs, and source snapshots.
- Verified a local plugin install/list/cache-comparison/remove cycle.
- Added original project artwork, Korean onboarding, and an MIT license.

This is a private development preview, not a stable release or a claim of universal correctness. The latest inspected hosted CI attempt was blocked before execution by GitHub's reported billing or spending-limit restriction; see the [dated release-readiness evidence](docs/RELEASE-READINESS.md). Comparative results must be read with their sample size and limitations.
