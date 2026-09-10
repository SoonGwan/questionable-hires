# Local plugin installation check

Executed with Codex CLI `0.153.4` on macOS, 2026-09-10 UTC (2026-09-11 in Seoul).

## Actual sequence

1. Built a bundle with `python3 scripts/build.py --output dist/bundle`.
2. Ran the official plugin-creator validator against `dist/bundle/plugins/questionable-hires`: passed.
3. Confirmed no marketplace named `personal` was registered before the test.
4. Ran `codex plugin marketplace add <absolute-bundle-path> --json`: returned `marketplaceName: personal`, `alreadyAdded: false`.
5. Ran `codex plugin add questionable-hires@personal --json`: returned version `0.1.0` and an installed cache path.
6. Ran `codex plugin list --marketplace personal --json`: reported `installed: true`, `enabled: true`.
7. Compared each of the eight cached skill directories with its source using `diff -rq`: no differences.
8. Removed only the test installation with `codex plugin remove questionable-hires@personal --json`, then removed its test marketplace registration with `codex plugin marketplace remove personal --json`.
9. Confirmed the marketplace list returned to its prior state: only the existing `openai-primary-runtime` source remained.

The generated bundle remains available for inspection or another installation. No pre-existing plugin or marketplace was removed. The test cache was generated from repository files and is reproducible by rebuilding and installing.

## What this proves

The local bundle resolves, installs, appears enabled, preserves the eight skill files, and can be removed through the CLI on this environment. Actual skill behavior and automatic selection were evaluated separately through repository-local skill discovery; see the [Astra report](../benchmarks/REPORT.md).

This is not a remote Git marketplace test, a public directory submission, or a guarantee for other host versions. The default bundle uses the marketplace name `personal`; do not replace an existing source with that name to repeat this test.
