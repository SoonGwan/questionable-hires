# Receipt for an existing fix

Reuse valid evidence; otherwise compare implementations in isolated copies with
**the same current regression assertions/inputs**, comparable configuration and
dependencies. Identify loaded revisions. Old-interface/setup failures are not
reproduction: disclose incompatibility, not a substituted check. Entrypoint scope,
runtime, exit-status and stopping rules apply; do not install missing dependencies.
Retrospective comparison cannot satisfy a request to run failure before editing.

Follow located tests' imports/inputs to select necessary support/configuration;
list only unresolved paths, not the whole repository again. Known support
directories can be selected directly; selection size does not prove completeness.

## Execute the comparison

For supported local Python layouts, prefer the helper over rewriting copy setup,
same-process import checks, execution and cleanup. Invoke it without reading its
source unless adapting/diagnosing it. Use native isolation for unsupported runtimes,
added/deleted implementation layouts or retained-copy requirements.

Choose **one** example and adapt paths, tests and revisions. Neither writes a
recipe, commits, stashes or reverses user patches; HEAD/HEAD^ are examples only.

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

- `fixed`: current tests/data/config/local dependencies, files or directories
  (including hidden leaves). Frozen once and shared across copies; `fixed_sha256`
  identifies leaves. Select only required, permitted inputs.
- `vary`: implementation files, required in both variants. `before`/string `after`
  resolve and report full commit IDs; no separate revision lookup is needed.
  Working-tree `after` freezes current bytes/modes, **not staged content**;
  `revisions.after=null`, `working_tree_after` hashes/modes identify selected files,
  not a commit or whole-repository snapshot.
- Optional `watch`, e.g. `"watch":["notes.txt"]`: existing files/directories to
  check but **not copy/execute**. `originals` reports all selected hashes/modes and
  unchanged status; `comparison_copies_removed` reports owned-copy cleanup.
  Reuse these checks rather than wrapping duplicates. New files, Git status or
  whole-repository integrity still require separate checks when requested.
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

JSON is compact by default; `--pretty` restores indentation for human reading.
Both retain identical fields and verbatim captured test-output strings.

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

Python 3.9+/POSIX; trusted tests only, **not a sandbox**. Copies are project-local
and removed; changed selected originals abort without restoration. Watch covers
existing leaves, not new directory entries or arbitrary side effects. Explicit
test paths/subprocesses can escape defaults; concurrent snapshots are not atomic.

Limits: shared 20 MB snapshot budget, 30 seconds/check (`--timeout` up to 300),
last 12,000 output characters. Known overflow rejects before reading; reads stop
at remaining budget + 1 byte and growth beyond budget aborts before tests. Final
integrity reads stop at original length + 1. Total memory is not bounded by this.
Child exit has a separate five-second cleanup wait; unconfirmed exit means CLI 2,
comparison not established and no next comparison. Other errors/interruptions
propagate. Descendant termination is not guaranteed; do not retry automatically
while a prior process may remain.
