# Release readiness — development preview

Checked 2026-09-11 against local commit `dd10633` and read-only GitHub API
responses. This is a release gate, not a claim of perfection or authorization to
publish. Preserve the eight coworker identities and report adverse evaluations.

Local follow-up at `67a6e35`: 186 tests pass in 26.506 seconds after installer
rollback improvements and expanded distribution tests. All eight installed skill
trees match source resource sets, bytes and permission bits; standalone and
marketplace skill trees match each other. All five installed helper entrypoints
run `--help` under isolated Python (`-I`) outside the source checkout. These are
temporary-directory tests, not a host installation, full helper execution or a
new remote CI result. The dated remote audit below remains unchanged.

Distribution follow-up at `d3901da`: the existing full suite passes 188 tests
(31.752 seconds), and two subsequently added CLI tests pass separately (0.810
seconds). The shipped scripts are copied into disposable source trees and run
under isolated Python: success, existing-target refusal, source-link rejection
and installer dry-run rejection preserve expected exit codes, readable errors,
existing bytes and external fixture contents. These fixtures do not validate
marketplace schema or host registration; those remain separate checks. Source
links are now rejected by both standalone installation and bundle building.

| Area | Evidence | State / next required check |
| --- | --- | --- |
| Local mechanics | 183 tests pass in 26.312 seconds after build recovery changes; catalog/link validation and diff checks pass | Passed locally; does not establish other platforms or model quality |
| Build recovery | Actual before-failure / after-pass tests for copy failure, cancellation, retry, original-error identity and existing destinations | Passed; cleanup can itself fail, leaving output |
| Standalone installation | Installer and rollback tests in the local suite | Current host discovery and other supported runtimes need separate evidence |
| Plugin installation | [Recorded local cycle](INSTALLATION-TEST.md), CLI 0.153.4, 2026-09-10 UTC | Historical snapshot only; no claim that the latest bundle was installed |
| Model efficiency | [Current candidate evidence](../benchmarks/CURRENT-CANDIDATE-STATUS.md) | Unmet across all eight skills; a favorable packaging pair is not sufficient |
| Automatic selection | [Original evaluation](../benchmarks/REPORT.md) | Broader unrelated prompts and current-resource selection remain to be checked |
| Browser interaction | Roadmap requires rendered interaction flows | Missing release-level evidence |
| Hosted CI | Latest retrieved run is [34503302864](https://github.com/SoonGwan/questionable-hires/actions/runs/34503302864), source `e441eb7`, created 2026-09-10 16:38:06 UTC | Failed before steps started; not a test failure and not a check of local `dd10633` |
| Remote distribution | No verified remote Git marketplace install | Do not advertise as tested |
| Publication | GitHub API reports `isPrivate: true` | Owner approval required for visibility change and release publication |

## Hosted CI evidence

The latest run's job `102959131919` has no executed steps and no assigned runner.
Its check annotation reports failed recent payments or a spending limit requiring
increase. These are GitHub's alternatives, not a diagnosis of which account
setting is responsible. The preceding two retrieved runs also conclude failure.
No workflow rerun, push, billing change or visibility change was performed.

Once the owner resolves that external restriction and authorizes pushing the
candidate, obtain a successful hosted run **for the intended release commit**.
Do not substitute a historical install, a different commit's CI, local green
tests or a badge for that evidence.

## Local work can continue

Keep improving realistic developer tasks and verify documentation against shipped
resources. Before publication, review included evaluation artifacts for sensitive
data, verify fresh-install instructions with the intended host, and synchronize
English/Korean claims. Installation into the owner's host and remote publication
are not implied by a local test pass.
