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

For small local Python comparisons, the installed helper handles copying,
import provenance and cleanup. Invoke it without reading its source unless
adaptation is needed. Adapt this recipe to actual files, commits and test arguments:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --spec - <<'JSON'
{"fixed":["test_parser.py"],"vary":["parser.py"],"before":"HEAD^","after":"HEAD","imports":["parser"],"runner":"unittest","tests":["-v","test_parser"]}
JSON
```

`fixed`: current tests, inputs, configuration and local dependencies. Files or
directories such as `["tests","samples","pyproject.toml"]` are accepted;
directories expand to regular files, including hidden files. Select only needed,
permitted inputs. Root selection, Git internals, symlinks, empty directories and
overlapping selections are rejected; traversal is bounded to 10,000 entries.
Each leaf is frozen once, shared by both implementations and hashed in
`fixed_sha256`.

`vary`: explicit implementation **files** from each commit, not directories.
Both lists must be nonempty, canonical project-relative and disjoint after
expansion: fixed directories cannot contain varying files. Listed imports must
resolve inside each copy. Launch with the project interpreter; checks reuse it
(`--python` overrides this when necessary). Use unittest or installed pytest;
other runtimes/custom runners require native isolated comparison instead.
Pass the intended revision expressions directly: the helper resolves and reports
full commit IDs, so a separate hash-resolution call is unnecessary. `HEAD^` is
only an example, not a rule for selecting the correct before implementation.

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

Child-exit confirmation has a separate five-second cleanup wait. Unconfirmed exit
means comparison-not-established (CLI exit 2) and no later comparison; existing
interruptions/errors propagate. Termination/descendant containment is not
guaranteed: don't retry automatically while a previous process may remain.
