# Receipt for an existing fix

Compare isolated implementations with **the same current assertions/inputs** and
comparable dependencies/configuration; reuse valid evidence. Identify loaded
revisions. Setup/old-interface failures are not defect reproduction. Preserve
entrypoint scope and stopping rules; do not install dependencies. Retrospective
comparison does not satisfy a requirement to observe failure before editing.

Select support/configuration from actual test imports/inputs. List unresolved
paths only; select known directories directly. Selection size is not completeness.

## Execute the comparison

For supported Python layouts, use the helper's copying, same-process import
checks and cleanup; inspect source only for adaptation/diagnosis. Use native
isolation for unsupported runtimes, added/deleted implementations or retained copies.

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
  `comparison_copies_removed` gives cleanup. Reuse those checks; new entries,
  Git status and whole-repository integrity need separate checks when requested.
- Selections must be canonical project-relative, unique and disjoint after
  expansion; no root, Git internals, symlinks, empty directories or overlap.
  `fixed`/`vary` must be nonempty. Directory traversal: at most 10,000 entries.
- `imports` must resolve inside each native test process's copy. Use the project
  interpreter (default: launching Python; override `--python` if needed), unittest
  or already-installed pytest. Child temp defaults are inside each copy: do not
  redirect global TMPDIR merely to localize checks or other launchers may pollute it.
- Optional `"import_roots":["src"]` supports regular source-layout packages.
  Select needed package initializers/support in `fixed` and implementations in
  `vary`; each root must contain selected files. Ordered canonical directories
  are prepended inside each copy before its root and reported in the result.
  No inherited `PYTHONPATH`, editable install, build hook or installed metadata
  is supplied. Use the native project setup when those are required.

## Read the evidence, not just the exit code

Use default compact JSON for agent execution; it retains every field and native
output. Reserve `--pretty` for a human-readable JSON request, not extra evidence.

CLI 0 means observations collected, **not proof**. Inspect each actual assertion,
requested test identity, before failure/after pass, copied-import evidence,
`exit_code`, `timed_out` and `output_truncated`. Help/version output is not execution.
Unittest zero/all-skipped runs return check 5; failures return 1, partial-skip
success 0. This guard does not prove requested coverage. Pytest keeps native exits.
Listed-module import exceptions, including `SystemExit(0)`, retain a traceback
and reserve check exit 7 for incomplete setup; no next comparison runs and CLI
returns 2. A runner independently exiting 7 is conservatively incomplete too.
This catches ordinary Python import exceptions, not `os._exit`, later runner
early exits or adversarial execution. Inspect actual test evidence regardless.

Python 3.9+/POSIX, trusted tests only: **not a sandbox**. Project-local copies are
removed; changed selected originals abort without restoration. Watch excludes new
entries/arbitrary effects. Test paths/subprocesses can escape; snapshots aren't atomic.

Limits: shared 20 MB snapshot budget, 30 seconds/check (`--timeout` up to 300),
last 12,000 output characters. Known overflow rejects before reading; reads stop
at remaining budget + 1 byte and growth beyond budget aborts before tests. Final
integrity reads stop at original length + 1. Total memory is not bounded by this.
Child exit has a separate five-second cleanup wait; unconfirmed exit means CLI 2,
comparison not established and no next comparison. Other errors/interruptions
propagate. Descendant termination is not guaranteed; do not retry automatically
while a prior process may remain.

Checks must finish their required work in the foreground. Once the direct native
runner exits, remaining members of its process group are killed and buffered
output drained under the original deadline; an inherited pipe alone no longer
turns a finished check into a timeout. Exit detection polls every 50 ms, subject
to scheduling. Background jobs intended to outlive the test runner are unsupported.
Tests still own assertions and orderly cleanup; escaped groups are not contained.
