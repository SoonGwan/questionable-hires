# Receipt for an existing fix

Compare isolated implementations with **the same current assertions/inputs** and
comparable dependencies/configuration; reuse valid evidence. Identify loaded
revisions. Setup/old-interface failures are not defect reproduction. Preserve
entrypoint scope and stopping rules; do not install dependencies. Retrospective
comparison does not satisfy a requirement to observe failure before editing.

Select support/configuration from actual test imports/inputs. List unresolved
paths only; select known directories directly. Selection size is not completeness.

## Execute the comparison

Reuse a project-native comparison that already establishes the required isolation,
assertions, loaded code and preservation. The Python helper is an option when its
copying, same-process import checks and cleanup replace missing setup; supporting
the language alone is not a reason to replace an adequate existing runner.
Native isolation is also valid, and necessary for unsupported runtimes,
added/deleted implementations or retained copies. Keep the same evidence requirements
whichever path is chosen. Read implementation for a concrete trust, adaptation or
diagnosis question; the CLI recipes below do not require importing the helper API.

For a required project-native workflow that lacks original-tree checks, optional
[native preservation support](native-preservation.md) reuses the guard without
replacing that workflow. It does not supply copying, execution or import evidence.

When verification must preserve Git metadata too, use
`git --no-optional-locks -c diff.autoRefreshIndex=false` for status/diff review.
This suppresses optional index refresh, not other command/driver side effects;
it does not make mutating commands read-only or change persistent Git settings.

Adapt **one** example's paths/tests/revisions; HEAD/HEAD^ are placeholders.
Neither writes a recipe, commits, stashes nor reverses user patches.

Committed fix:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --spec - <<'JSON'
{"fixed":["test_parser.py"],"vary":["parser.py"],"before":"HEAD^","after":"HEAD","imports":["parser"],"runner":"unittest","tests":["-v","test_parser"]}
JSON
```

Already-present uncommitted fix:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --spec - <<'JSON'
{"fixed":["test_parser.py"],"vary":["parser.py"],"before":"HEAD","after":{"working_tree":true},"imports":["parser"],"runner":"unittest","tests":["-v","test_parser"]}
JSON
```

- `fixed`: required, permitted current tests/data/config/dependencies, files or
  directories including hidden leaves. Frozen once for both copies; leaf hashes
  appear in `fixed_sha256`.
- `vary`: implementation files, required in both variants. `before`/string `after`
  resolve and report full commit IDs; no separate revision lookup is needed.
  Working-tree `after` freezes current bytes/modes, **not staged content**;
  `revisions.after=null`, `working_tree_after` hashes/modes identify selected files,
  not a commit or whole-repository snapshot.
- Optional `"watch":["notes.txt"]`: existing files/directories checked, **not
  copied/executed**. `originals` gives selected hashes/modes/unchanged status;
  `comparison_copies_removed` gives cleanup. Reuse those selected-file checks.
- Optional `"guard_tree":true`: only for requested whole-project preservation
  with all reads authorized. Checks Git/ignored entries, bytes/modes and link text
  around comparison; changes abort without restoration. It excludes link targets,
  timestamps/other metadata, concurrent or restored changes and other commands.
  `tree_guard` reports counts/digest; limits are 10,000 entries/20 MB per inventory.
  See [guard details](comparison-details.md#preservation-guards) for boundary questions.
- Selections must be canonical project-relative, unique and disjoint after
  expansion; no root, Git internals, symlinks, empty directories or overlap.
  `fixed`/`vary` must be nonempty. Directory traversal: at most 10,000 entries.
- `imports` must resolve inside each native test process's copy. Use the project
  interpreter (default: launching Python; override `--python` if needed), unittest
  or already-installed pytest. Pytest verifies imports after native collection,
  before test bodies, preserving configuration and assertion rewriting.
  Child temp defaults are inside each copy: do not
  redirect global TMPDIR merely to localize checks or other launchers may pollute it.
- For a dynamically loaded module held by a declared import, optional
  `"module_bindings":{"test_loader:component":"plugin.py"}` checks that module's
  `__file__` against the selected fixed/varying file in the same native process.
  `test_loader` must also be in `imports`. Dotted attributes traverse module
  dictionaries only: no expressions, properties, arbitrary objects or function
  identity checks. Missing/wrong bindings produce incomplete evidence before
  tests, not regression failures. Checks occur before unittest execution or after
  pytest collection; fixtures/later reassignment and actual dispatch require
  project-native assertions. Plain `imports` verifies modules, not their attributes.
- Optional `"invocation":"module"`: for required `python -B -m unittest ...`,
  with `runner: "unittest"` and existing `tests`; no internal adapter needed.
  Default is `bootstrap`. Copy-local startup checks imports in the native test
  process; inspect `command`, `native_exit_code` and `provenance_ready`.
  Conventional existing system/user hooks are preserved. Project-local or unusual
  startup customization needs native project setup, not a bypass; read
  [startup compatibility](comparison-details.md#native-module-startup) when applicable.
- Optional `"import_roots":["src"]` supports regular source-layout packages.
  Select initializers/support too; each root must contain selected files.
  Ordered canonical roots precede each copy's root and appear in the result.
  No inherited PYTHONPATH, editable install, build hook or installed metadata;
  use native project setup when required.

## Read the evidence, not just the exit code

Use default compact JSON for agent execution; it retains every field and native
output. Reserve `--pretty` for a human-readable JSON request, not extra evidence.

CLI 0 means observations collected, **not proof**. Inspect each actual assertion,
requested test identity, before failure/after pass, copied-import evidence,
`exit_code`, `timed_out` and `output_truncated`. Help/version output is not execution.
Each `Verified copied import:` line includes the resolved module `path` and native
process `pid`. This records import-time location, not proof against subsequent
monkey-patching; a truncated line is unavailable evidence, not permission to infer it.
Skipped/empty checks do not establish a regression, even with native exit 0.
Missing import/startup provenance or check exit 7 means incomplete: CLI 2, no next
comparison. Preserve native errors, not just the wrapper status. See
[exit interpretation](comparison-details.md#exit-interpretation) for runner-specific
counts, import errors or early-exit diagnosis.

Python 3.9+/POSIX, trusted tests only: **not a sandbox**. Copies are removed;
`originals` checks selected bytes/modes, not arbitrary effects or new entries.
Test paths/subprocesses can escape; snapshots are not atomic. Guard limitations
are detailed in [preservation guards](comparison-details.md#preservation-guards).

Copying: shared 20 MB budget; overflow aborts before tests, not a partial comparison.
Execution: 30 seconds/check (`--timeout` up to 300), last 12,000 output characters.
Required work must finish in the foreground: remaining process-group members are
killed after runner exit; persistent background jobs are unsupported. Cleanup can
wait five more seconds; unconfirmed exit means incomplete, no next comparison.
Do not retry automatically while prior work may remain. For budget, output or
cleanup questions read [resource/process boundaries](comparison-details.md#resource-and-process-boundaries).
