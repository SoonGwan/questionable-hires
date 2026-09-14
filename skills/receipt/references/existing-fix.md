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
  with all source reads authorized. Inventory Git/ignored files, directories
  (including empty/root), bytes/modes and link text, not link targets. `tree_guard`
  reports unchanged/counts/digest, not a full hash listing. Replaces snapshots
  around native comparison, not diff review/later checks. Added/removed/changed
  entries abort without restoration. No exclusions; special files/oversize fail
  closed: 10,000 entries including root, 20 MB streamed per inventory, separate
  from copying. Larger projects need another native method.
- Selections must be canonical project-relative, unique and disjoint after
  expansion; no root, Git internals, symlinks, empty directories or overlap.
  `fixed`/`vary` must be nonempty. Directory traversal: at most 10,000 entries.
- `imports` must resolve inside each native test process's copy. Use the project
  interpreter (default: launching Python; override `--python` if needed), unittest
  or already-installed pytest. Child temp defaults are inside each copy: do not
  redirect global TMPDIR merely to localize checks or other launchers may pollute it.
- Optional `"invocation":"module"`: for required `python -B -m unittest ...`,
  with `runner: "unittest"` and existing `tests`; no internal adapter needed.
  Default `bootstrap` is unchanged. Temporary copy-local startup checks same-process
  imports; results include `command`, `native_exit_code`, `provenance_ready`.
  Timeout/output supervision remains. Only child-local lookup changes; descendants
  don't inherit the probe. Required site/user hooks or disabled site initialization
  need native project setup instead.
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
Bootstrap unittest: failure 1, empty/all-skipped 5, partial-skip success 0.
Module mode preserves native exits, including **0 for empty/all-skipped**: inspect
counts/skips. Missing startup provenance reserves check 7, retaining the native
exit separately. Pytest keeps native exits. No mode proves requested coverage.
Listed import exceptions (including `SystemExit(0)`) retain tracebacks and reserve
check 7: CLI 2, no next comparison. Independent runner exit 7 is conservatively
incomplete too. This does not catch `os._exit`, later early exits or adversarial
execution; inspect actual tests.

Python 3.9+/POSIX, trusted tests only: **not a sandbox**. Project-local copies are
removed; changed selected originals abort without restoration. Watch excludes new
entries/arbitrary effects. Test paths/subprocesses can escape; snapshots aren't atomic.
Tree guards do not cover link targets, ownership, timestamps, ACLs/xattrs, concurrent
writes, changes restored between observations, or operations outside their interval.

Copying: shared 20 MB budget. Known overflow rejects before reading; reads stop at
remaining budget + 1 byte, growth overflow aborts before tests, final integrity
reads stop at original length + 1. Total memory is not bounded by these limits.
Execution: 30 seconds/check (`--timeout` up to 300), last 12,000 output characters.
Child exit has a separate five-second cleanup wait; unconfirmed exit means CLI 2,
comparison not established and no next comparison. Other errors/interruptions
propagate. Descendant termination is not guaranteed; do not retry automatically
while a prior process may remain.

Required work must finish in the foreground. After direct-runner exit, remaining
process-group members are killed and buffered output drained under the original
deadline; inherited pipes alone don't cause timeouts. Exit polling: 50 ms, subject
to scheduling. Persistent background jobs are unsupported; tests still own
assertions/cleanup and escaped groups aren't contained.
