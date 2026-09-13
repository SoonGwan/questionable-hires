# Release readiness — development preview

## 2026-09-14: Receipt comparison completion regression

The executable/test bytes committed as `a869f62` pass **429 local tests in
147.545s**, macOS/Python 3.9.6, with no reported failures or skips. No executable
edits or concurrent model benchmark ran during the suite. This includes the new
[native before/after inherited-pipe regression](../benchmarks/RECEIPT-PIPE-EXIT-01.md).
Local checkout evidence only: current hosted CI, Linux/source archives and the
Python version matrix are not reverified by this result. Prior checks remain below.

## 2026-09-14: full local regression after foreground-exit cleanup

Working tree at launch `ead49db`, macOS/Python 3.9.6:
`python3 -B -m unittest discover -s tests -v` passes **428 tests in 169.970s**,
exit 0, no reported failures or skips. No executable/test/resource changes or
concurrent model benchmark ran during the suite; only the hosted-status paragraph
below was committed while it ran.

Coverage includes all-eight build/install behavior, helper execution, fixture and
evaluator mechanics, and the new Exorcist inherited-pipe/Unicode-drain regression.
This is a local checkout result, not a current source-archive/Linux/Python-matrix
run, fresh dependency installation, hosted CI success or model-performance proof.
Historical archive and platform checks below retain their original revisions.

## 2026-09-14: current hosted gate rechecked

Read-only check of `ead49db` [run 34774733190](https://github.com/SoonGwan/questionable-hires/actions/runs/34774733190)
finds all four jobs concluded failure with no executed steps. Source-archive
check `103770654579` reports that recent account payments failed **or** the
spending limit needs increasing; the response does not determine which setting.
This is not an executed test failure or hosted verification of the current code.
Repository visibility is still private. No billing, publication or account
settings were changed. Local execution remains separate evidence.

## 2026-09-13: latest helper guards verified in the source distribution

The unmodified `5b78fef` archive passes validation, localized featured/chart
consistency and the full suite under local Linux arm64/Python 3.12.3:
**328 discovered, 326 passed, two explicit Git-provenance skips, 17.176 seconds**.
This includes current Receipt/Con Artist no-execution guards, bounded Receipt
reads, batch evidence retention, source-context selection and existing all-eight
build/install checks. No `.git` or ignored local runs are in the input archive.
No file overlays were used. The existing image ID and read-only host PyYAML mount
are the same as documented below; network access is disabled and no dependencies
were installed. The retained host archive is
`benchmarks/local-runs/linux-5b78fef.DCCRYx`; the container was disposable.

This is source-distribution behavior evidence, not a fresh dependency installation,
model performance measurement, hosted CI success or authorization to publish.
Read-only recheck of [hosted run 34743404198](https://github.com/SoonGwan/questionable-hires/actions/runs/34743404198)
at the same revision finds all four jobs failed with zero steps and no assigned
runner. The source-archive check `103686827727` explicitly reports failed recent
payments **or** a spending limit requiring increase. It does not establish which
setting is responsible. Repository visibility remains private. No account,
billing or publication settings were changed; the owner-side hosted gate remains.

## 2026-09-13: committed archive gate

The unmodified `92b49df` source archive passes the same network-disabled Linux
arm64/Python 3.12.3 check described below: 311 discovered, 309 passed, two explicit
Git-provenance skips (16.622 seconds). No test overlays were used.

`c2fd79e` adds a separate source-archive CI job alongside the existing checkout
matrix, so checkout history tests remain scheduled rather than being replaced
by skipped archive checks. The job archives `HEAD`, verifies `.git` and ignored
local-run state are absent, and runs validation, chart/localization checks and
the full test suite under Python 3.12. A real temporary-Git integration test
executes the workflow's Bash block itself: committed payload wins over dirty
working-tree content, untracked files are absent, and a deliberate validator
exit 7 stops subsequent checks without hiding the failure.

The complete unmodified `c2fd79e` archive, including that new test, also passes
locally in the same Linux image: **312 discovered, 310 passed, two explicit
Git-provenance skips (16.757 seconds)**. The only external test dependency is
the existing read-only PyYAML mount; there are no overlays, downloaded packages,
network access or checkout history. Source archive checks and packaging checks
are not new model efficiency evidence. The new hosted job remains unverified
until GitHub's account restriction is resolved; adding a job does not bypass it.

## 2026-09-13: current Linux archive check and hosted gate

Read-only hosted check of `10d416f`: [run 34741549262](https://github.com/SoonGwan/questionable-hires/actions/runs/34741549262)
concluded failure with zero executed steps and no assigned runner in both Python
jobs (`103681980852`, `103681980904`). Both annotations report failed recent
payments **or** a spending limit requiring increase; this does not identify which
account setting is responsible. No billing, visibility or release changes were
made. The hosted gate remains unresolved, not a demonstrated code failure.

Unlike the older feasibility check below, the local Docker endpoint is now live.
Using the already-present browser image, Linux arm64/Python 3.12.3 tests ran with
network disabled and a read-only source archive copied into a disposable
container. Image ID:
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
Its Python lacked PyYAML, so the existing host PyYAML 6.0.3 package was mounted
read-only and used in pure-Python mode (`__with_libyaml__ = False`). No dependency
was downloaded. The first `/tmp` mount was unavailable inside the Docker VM;
the archive was relocated to the shared workspace before any tests ran.

The unmodified `10d416f` archive discovered 311 tests and exposed three failures:
zero-test unittest discovery returned 5 instead of 0; the output-limit test
contained no actual test; and invoice-control evidence assumed one unittest
display format. Fixes accept the explicit no-tests status only alongside zero
discovery, exercise a real passing test for output limits, and recognize both
qualified method labels while still requiring each named control to pass.
No frozen model fixture or reported benchmark score was changed.

Rechecking the same archive with only those three test-file corrections passes
validation/localization checks: **311 discovered, 309 passed, two explicit
Git-provenance skips, 16.547 seconds**. The skipped checks are the existing
packaging source/review history comparisons; their archived behavioral tests
still run. All eight build/install resource checks run inside this suite.
This is local Linux source-distribution evidence, not hosted CI, a pristine
dependency install, a model benchmark or verification on Python 3.9/3.11 Linux.
The workflow now also schedules 3.12 to catch these failures once the account
restriction is resolved. Scheduling is not execution evidence.

Owned archive copies remain under ignored local runs for reproducibility;
containers used `--rm`. No persistent container, image, host installation,
production service or account setting was changed by this check.

## Earlier evidence (each entry retains its original revision)

Checked 2026-09-11 against local commit `dd10633` and read-only GitHub API
responses. This is a release gate, not a claim of perfection or authorization to
publish. Preserve the eight coworker identities and report adverse evaluations.

Pre-publication audit on 2026-09-12 KST at `57485a2`: a filename-only scan of
every reachable Git revision found zero files matching common private-key,
GitHub-token, OpenAI-key or bearer-token patterns. This is a bounded pattern scan,
not proof that history contains no sensitive prose. A `git archive HEAD`
extraction with no `.git` passed catalog/link/form validation, featured-chart and
localized-README synchronization, and discovered 261 tests: 259 executed and
passed, while two Git-history provenance comparisons skipped explicitly. No
ignored local model logs or browser dependencies were present in the archive.

The latest hosted run at `57485a2` scheduled Python 3.9 and 3.11, but both jobs
ended with zero executed steps. This remains an external GitHub Actions gate, not
a test failure or passing Linux evidence. Repository visibility is still private,
there is no tag or GitHub Release, and the owner must explicitly authorize both
visibility and release publication.

Latest full local run on 2026-09-12 KST at `254e703`: **240 tests pass in
38.612 seconds** on local macOS/Python 3.9.6. This includes replaying both exported
nested-interaction projects outside the checkout without private logs or Git.
It is not a source-archive run, a hosted Linux result, or model performance
evidence. No new model sessions were launched for this regression run.

Historical full local run at the `fb5b9a0` content snapshot: 215 tests pass in
31.909 seconds, including the exported Landlord evidence audit. That evidence
audit also passes in a disposable directory containing no Git history or private
logs. Model efficiency remains unmet; inspect the current candidate link below.

Latest distribution follow-up adds real bundled Exorcist execution outside the
checkout under isolated Python (`-I`): success, child exit 124 mapping to CLI 1,
and a SIGTERM-ignoring child killed on deadline with output retained and direct
child cleanup confirmed. The unrelated project's sentinel remains unchanged.
Eight build, fourteen install and two distribution-CLI tests pass separately
(24 total), along with repository validation. The build tests also execute the
current Receipt helper on real before/after Git revisions and compare all eight
shipped resource trees against source bytes/modes. This is disposable local
distribution evidence, not owner-host registration, descendant containment,
remote installation or current hosted CI.

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

Latest local full run after source/output separation (`132fa49` executable
snapshot): 192 tests pass in 32.564 seconds, including the CLI tests and both
self-copy rejection regressions. Contributor instructions distinguish these local
checks from model-usage evaluations; issue forms parse as YAML with unique field
IDs. No hosted workflow or model benchmark was run for this documentation update.

Issue-form validation follow-up at `292bd62`: 194 local tests pass (32.713
seconds). Malformed/missing forms, duplicate IDs, missing types, blank labels and
string-valued required flags produce diagnostics. This validates the maintained
forms' local consistency, not GitHub's complete schema or rendered UI.

Source-archive check at `539e39a`: `git archive HEAD` extracted to a disposable
directory with no `.git` passes catalog/link/form validation and the full suite:
196 discovered, 195 executed/passed, one explicit pinned-source provenance skip
(26.201 seconds). The first archive check at `773a9ef` found three HTTPX snapshot
test errors and one collector benchmark failure caused by reliance on checkout
history. Those tests now create their own real temporary Git commits; they are
not skipped. This is local macOS/Python evidence, not a hosted Linux CI run.

Current source-archive follow-up at `71dbcae`: validation passes and 209 tests
are discovered; 207 execute/pass and two provenance comparisons explicitly skip
(30.491 seconds). Both packaging behavior regressions now execute without
checkout history. The earlier `ed780b0` archive run discovered 207 tests with two
skips, but one skip incorrectly covered the entire packaging-review regression.
`30bf7bb` replaced that dependency with an archived two-file overlay; `71dbcae`
adds a subprocess regression that omits both .git and the historical exporter.
With history available, overlay reconstruction was separately verified against
the actual `436e409` source. No hosted CI, browser or model run is included in this
archive result. Temporary extraction directories were removed after execution.

| Area | Evidence | State / next required check |
| --- | --- | --- |
| Local mechanics | 240 tests pass in 38.612 seconds at `254e703`; includes exported nested-interaction replay | Passed locally on macOS/Python 3.9.6; does not establish Linux, current source-archive behavior, host installation or model quality |
| Build recovery | Actual before-failure / after-pass tests for copy failure, cancellation, retry, original-error identity and existing destinations | Passed; cleanup can itself fail, leaving output |
| Standalone installation | Installer and rollback tests in the local suite | Current host discovery and other supported runtimes need separate evidence |
| Plugin installation | [Recorded local cycle](INSTALLATION-TEST.md), CLI 0.153.4, 2026-09-10 UTC | Historical snapshot only; no claim that the latest bundle was installed |
| Model efficiency | [Current candidate evidence](../benchmarks/CURRENT-CANDIDATE-STATUS.md) | Unmet across all eight skills; a favorable packaging pair is not sufficient |
| Automatic selection | [Two negative requests](../benchmarks/ROUTING-NEGATIVE-01.md) and [two positive comparisons](../benchmarks/CURRENT-SELECTION-01.md) with the current bundle | Relevant Landlord/Receipt selection observed; incidental cross-skill reference access in broad search; ambiguous prompts and other six hires' current recall remain open |
| Browser interaction | [Browser-generated input](../benchmarks/BROWSER-INPUT-01.md) distinguishes broken/guarded behavior with fill/keyboard, normal results, focus, error recovery and same-document view disposal; workflow watchdog tested at normal and short deadlines | Partial: synthetic sequences only; full-document navigation and model QA missing; in-process timer is not an OS supervisor; hung-close injection and original dump-DOM timeout diagnosis remain open |
| Hosted CI | Latest retrieved run is [34503302864](https://github.com/SoonGwan/questionable-hires/actions/runs/34503302864), source `e441eb7`, created 2026-09-10 16:38:06 UTC | Failed before steps started; not a test failure and not a check of local `dd10633` |
| Remote distribution | No verified remote Git marketplace install | Do not advertise as tested |
| Publication | GitHub API reports `isPrivate: true` | Owner approval required for visibility change and release publication |

## Latest source archive

[Linux container browser check](../benchmarks/BROWSER-CONTAINER-01.md): after
explicit owner authorization, the pinned Playwright 1.63.0 image ran all six
existing browser variants on Linux arm64 with networking disabled and the checkout
read-only. This establishes an author-side container runtime, not model-driven QA,
host installation, hosted CI or skill efficiency. Colima and the pulled image
remain locally available.

Source archive at `a61fec7`, checked 2026-09-12 KST: validation passes;
243 tests discovered, **241 executed/passed and two explicit provenance-only
skips**, in 36.940 seconds on local macOS/Python 3.9.6. The skipped comparisons
are pinned packaging-review provenance and pinned source history; archived
fixture behavior still runs. Extraction contains no `.git`, private local-run
logs or browser node_modules. It includes current browser staging/status tests
using synthetic dependencies and actual exported interaction replay. It does
not launch a model or execute the optional Chrome workflow. The owned extraction
was removed. This supersedes older archive counts below, not hosted-CI or model
performance evidence.

Browser follow-up: the [clearing regression](../benchmarks/BROWSER-CLEAR-01.md)
executes actual fill and keyboard clearing in six Chrome contexts, distinguishing
stale overwrite from a working request guard while retaining prior input,
recovery and same-document disposal checks. This is author-side synthetic browser
evidence, not model QA or full-document navigation coverage.

Python-version follow-up on 2026-09-12 KST: local macOS Python 3.11.16 initially
failed because PyYAML was absent and one Receipt test matched Python 3.9's exact
unittest name formatting. The regression now checks an explicit marker emitted
only after the child asserts its interpreter identity; before/after statuses and
test counts remain checked. In a new temporary 3.11 virtual environment with the
declared dependency (PyYAML 6.0.3), validation and all 237 tests pass (35.715 seconds).
The 23 Receipt tests also pass on Python 3.9.6 (7.235 seconds). The temporary
environment was removed; no host package installation or model run was performed.
This is macOS compatibility evidence, not Linux hosted-CI success or a skill
performance improvement. Historical archive counts below remain snapshot-specific.

Current distribution follow-up: the built Con Artist CLI executes a real two-fault
batch from an unrelated working directory under isolated Python (`-I`). Removing
the write and duplicating the write both survive the existing weak test; the same
stronger assertion passes on correct code and fails with AssertionError on each
mutant. Copied-import evidence, nontruncated outputs and the second audit's direct
baseline-observation reference are checked. Original file bytes remain unchanged
and disposable copies are removed.

The built Friday CLI also runs three real in-memory SQLite phases (before, rename
migration with new data, rollback): compatible reader rows are checked, while
incompatible readers retain query errors despite the completed matrix's exit 0.
The built Necromancer CLI collects attribution and the introducing patch from a
disposable two-commit Git repository. Both run outside the checkout with isolated
Python; project bytes, including Git files for the history check, stay unchanged.
All eleven build tests pass; no model performance or host-registration claim
follows from these local package executions.

Source archive rechecked at `05a9fce`: `git archive` extraction without `.git`
passes validation and discovers 235 tests; 233 execute/pass and the two pinned
Git-provenance comparisons skip explicitly (35.925 seconds). This includes all
five bundled helper execution checks, current mutation-probe reuse regressions,
the executable two-fault example and shipped Landlord evidence checks. The
documented example CLI also executes separately from the extraction: both weak
tests miss their faults, both stronger probes capture the intended AssertionError,
and the second audit references the first correct-code observations.
The extraction has no ignored local-run logs or installed browser dependencies;
the optional browser workflow and fresh model evaluations are not part of this
Python test result. The owned extraction is removed after execution. This updates
the local archive evidence, not the historical hosted-CI result below.

## Hosted CI evidence

The validation workflow now schedules Python 3.9 and 3.11 separately with matrix
fail-fast disabled, so a version-specific failure does not cancel the other
version's evidence. This addresses the locally reproduced unittest-format issue;
it is a configuration change, not two passing hosted runs. A 2026-09-12 KST local
Linux feasibility check found no running Docker endpoint. No daemon was started,
image pulled, host configuration changed or workflow rerun. Local Python 3.11
coverage above remains macOS-only; both intended Linux jobs still need execution
on the release revision after the external CI restriction is resolved.

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
