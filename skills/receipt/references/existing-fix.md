# Receipt for a fix that already exists

Reuse valid existing evidence. Otherwise freeze the current regression assertion
and inputs in isolated copies; vary implementation, **not each revision's tests**.
Keep dependencies/configuration comparable and identify the loaded revisions.
An old-interface/setup failure is not reproduction: disclose incompatibility
instead of substituting a different check. The entrypoint's runtime, scope,
exit-status and stopping rules still apply; do not install missing dependencies.

Once the runner, regression and fix are located, follow their imports and input
references to select supporting files. Narrow listings to unresolved paths;
don't inventory the repository again merely to construct a copy recipe. A known,
appropriate support directory can be selected directly. Still inspect required
configuration and cooperating code; a short selection is not proof that all
required inputs are present. The entrypoint's instruction-discovery boundary
applies here too.

## Optional Python comparison helper

For local unittest/installed-pytest comparisons within the limits below, prefer
the helper to rebuilding copy setup, same-process import checks, execution and
cleanup. Existing valid evidence still takes precedence. Use native comparison
when the required layout/runtime or retained-copy workflow is unsupported.
If the task requires broader original-file integrity checks, add those around
the helper; its selected-file checks do not cover the whole repository. That
gap alone need not duplicate the entire comparison pipeline. Invoke the helper
without reading its source unless adapting or diagnosing it.

Choose the implementation source explicitly; adapt paths and test arguments.
For a **committed fix**, compare the appropriate two commits:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --spec - <<'JSON'
{"fixed":["test_parser.py"],"vary":["parser.py"],"before":"HEAD^","after":"HEAD","imports":["parser"],"runner":"unittest","tests":["-v","test_parser"]}
JSON
```

For an **already-present uncommitted fix**, freeze current implementation bytes:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --spec - <<'JSON'
{"fixed":["test_parser.py"],"vary":["parser.py"],"before":"HEAD","after":{"working_tree":true},"imports":["parser"],"runner":"unittest","tests":["-v","test_parser"]}
JSON
```

Neither example creates a recipe file, commit or stash. Do not run both merely
because both are shown. `HEAD`/`HEAD^` are examples, not inferred correct revisions.

`fixed`: current tests, inputs, configuration and local dependencies. Files or
directories such as `["tests","samples","pyproject.toml"]` are accepted;
directories expand to regular files, including hidden files. Select only needed,
permitted inputs. Root selection, Git internals, symlinks, empty directories and
overlapping selections are rejected; traversal is bounded to 10,000 entries.
Each leaf is frozen once, shared by both implementations and hashed in
`fixed_sha256`.

`vary`: explicit implementation **files**, not directories.
Both lists must be nonempty, canonical project-relative and disjoint after
expansion: fixed directories cannot contain varying files. Listed imports must
resolve inside each copy. Launch with the project interpreter; checks reuse it
(`--python` overrides this when necessary). Use unittest or installed pytest;
other runtimes/custom runners require native isolated comparison instead.
Pass the intended revision expressions directly: the helper resolves and reports
full commit IDs, so a separate hash-resolution call is unnecessary.

The working-tree variant freezes selected current implementation bytes and modes
once alongside current tests/support, then runs both copies. It does not commit, stash, read staged
implementation content or reverse a working-tree patch. `revisions.after` is null;
`working_tree_after.sha256` and `.modes` identify the selected snapshot, not a Git
commit or the whole repository. Normal Git revision strings retain their meaning.
Both variants still require each selected file; added/deleted implementation
layouts need native comparison. This retrospective check does not satisfy a
request to execute a failure **before making** the original edit. It is not an
atomic snapshot of concurrently changing files.

Python 3.9+, POSIX; 20 MB snapshot budget, 30 seconds/check (`--timeout` up to 300),
last 12,000 output characters. Copies are project-local and cleaned; selected
original bytes/permissions are checked, not every side effect. Original changes
are reported, never restored. Trusted tests only, **not a sandbox**. The byte
budget rejects known-overflow working files before reading/comparing and bounds
each working-file read to the remaining budget plus one overflow byte. Growth
beyond that budget aborts before test execution. Final integrity reads are bounded
to the original file length plus one byte; detected changes are not restored.
This does not bound total memory
or provide an atomic snapshot against concurrent writes. JSON retains
revisions, leaf hashes and separate outputs/statuses. CLI exit 0 means collected
observations, **not proof**: inspect the actual assertion failure, after pass,
provenance, timeout and truncation fields before claiming the fix.

For a normally completed unittest run, zero tests or an entirely skipped suite
produces check exit 5 with an explicit no-execution diagnostic. Real failures
retain exit 1; a passing suite with some skipped tests still exits 0. This guard
does not prove that the requested regression ran: inspect test identities and
outcomes, and never use runner help/version output as execution evidence.
Pytest retains its native exit behavior. The comparison CLI still distinguishes
collected observations from proof, so inspect each check rather than its outer exit.

Child-exit confirmation has a separate five-second cleanup wait. Unconfirmed exit
means comparison-not-established (CLI exit 2) and no later comparison; existing
interruptions/errors propagate. Termination/descendant containment is not
guaranteed: don't retry automatically while a previous process may remain.
