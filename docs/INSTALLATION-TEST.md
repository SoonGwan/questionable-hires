# Local plugin installation check

Current standalone CLI evidence is separate: [all-eight skills CLI installation](../benchmarks/SKILLS-CLI-INSTALL-01.md),
source `45fe88e`, `skills@1.5.26`, 2026-09-14. All 38 selected resource files and
modes match, seven Python entrypoints and both task-aware callback assets execute
from a disposable project. It is not the historical plugin registration below
or a remote authenticated installation.

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

## Installed helper behavior check — 2026-09-13

The standalone installer is also exercised outside the repository in
`tests/test_install.py::InstallTests.test_installed_component_probe_preserves_real_failure_through_wrapper`.
It installs Mother-in-law and Exorcist into a temporary skill directory, creates
a separate consumer project, then invokes both copied scripts with Python `-I -B`
from the consumer directory. No model session, dependency installation, network,
host discovery configuration or marketplace registration is involved.

The installed sequence probe runs through the installed process-deadline wrapper:

| Consumer implementation | Sequential control | Reversed completion | Final reversed state | Both CLI statuses |
| --- | --- | --- | --- | --- |
| Generation-guarded | pass | pass | `new result` | 0 |
| Unguarded assignment | pass | fail | `old result` | 1 |

The test checks the actual completion order, state, child/outer status and agreement
between captured JSON and the same execution's retained evidence file. It also
requires no timeout/truncation, confirmed direct-child cleanup, unchanged consumer
source and no extra project files. This guards against an installed helper that
prints help but cannot execute, or a wrapper hiding the child failure. It does
not certify browser behavior, all supported component interfaces, automatic skill
selection, or model efficiency. The test's temporary directories are cleaned up.

All seven shipped script entrypoints additionally execute `--help` from installed
copies under isolated Python; all eight hires' resources are compared byte-for-byte
and mode-for-mode with standalone and built-plugin copies. This supplements rather
than reruns or relabels the historical CLI installation record above.

## Read-only installation comparison — 2026-09-14

Previous source `be6ddeb`. `scripts/install.py --check` compares selected installed
skills to the local source checkout, without creating or updating installations.
This addresses copies that remain stale after a source pull, including newly added
resources such as Con Artist's focused native-probe guide. It does not fetch,
certify remote freshness, activate models, or label personal edits safe to replace.

Five new regression tests exercise missing destinations without creation; complete
all-eight installation matching; byte/mode differences, missing/new resources and
personal extra files without modification; cache exclusions and refusal to open
linked resources; real CLI JSON/exits for matching, different and invalid inputs.
All 20 installation tests pass in 1.777s. Existing installed helper behavior tests
remain, rather than replacing behavioral coverage with hash checks.
Full post-change validation: 509 tests pass in 74.941s, no failures/skips. The
pre-change 504-test suite also passed (74.456s). These are local checks, not hosted
CI or a model-efficiency experiment; neither duration is a claimed improvement.

Comparison failures emit no partial success report. Exit 0 is matching, 2 is
differences/missing installs, and 1 is a comparison failure. Normal argument parser
errors also use exit 2. Linked/special resources and unreadable files are not
silently skipped (generated Python cache exclusions mirror installation).
Use a trusted checkout not being changed concurrently; there is no race isolation.
Differences are reported for manual review, never automatically overwritten.

## Whole-bundle regression — 2026-09-14, source a636475

After the Friday sequence candidate and CLI-stream preservation changes,
`python3 -B -m unittest discover -s tests` passes **518 tests in 76.826s**, with
no failures or skips. This is a fresh local full-suite result, not a relabeling
of the earlier 509-test run. No model session was started by these unit tests;
printed synthetic schedule/completion messages exercise runner controls.

Included distribution coverage at this revision:

- All eight standalone copies preserve source resource bytes and modes, and the
  built marketplace's skill inventory matches the standalone inventory.
- All seven copied Python script entrypoints run `--help` under isolated Python
  outside the checkout; this checks executability, not every workflow.
- Actual installed Mother-in-law/Exorcist composition preserves both passing
  behavior and the intended stale-result failure, child/outer exits and evidence.
- Bundled Con Artist, Friday, Necromancer, Receipt and Exorcist checks execute
  actual recipes, history or processes; they are not only manifest assertions.
- Missing/different installation comparison, conflict preservation, failed-copy
  cleanup, native fixture failures and output-capture controls remain covered.

Repository/link validation and featured English/Korean synchronization checks
also pass. User installation/configuration was not changed. This is local macOS
evidence, not refreshed hosted CI, remote `npx` authentication, automatic skill
selection, a public-release certification or proof of all-eight model efficiency.
The test duration is recorded for reproducibility, not marketed as performance.
