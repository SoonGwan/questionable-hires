# Receipt for a fix that already exists

First determine whether available before/after evidence already establishes the
same input, assertion, implementation revisions and relevant failure. Reuse it
when valid; do not recreate history just because Receipt was invoked.

If comparison is needed, use isolated local copies without reversing patches in
the user's working tree. Freeze the regression assertion and inputs across both
versions: vary the affected implementation, **not each revision's historical test
suite**. Old tests may never have checked the reported boundary. Keep required
dependencies/configuration comparable and identify the actual loaded revision.

Run the same regression through the project's documented runtime and command.
Capture each exit status independently of later printing. Confirm that before
fails for the reported behavior, not an import/compiler/setup error, and after
passes. If an old interface cannot run the same check, name that limitation;
two different checks do not establish the claimed before/after result.

Verification does not authorize production edits, installations, external
services or publication. Preserve user changes. Return the decisive command,
revisions, behavior and limits; no separate report or complete history survey is
required. Stop after the scoped comparison, not after unrelated regression work.

## Optional Python comparison helper

For small, local Python repositories, run `scripts/compare.py` from the installed
Receipt directory instead of rewriting copy-and-test plumbing. Use the project's
interpreter; no need to read the helper implementation for normal invocation:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --python /path/to/project/python --spec - <<'JSON'
{"fixed":["test_totals.py"],"vary":["totals.py"],"before":"HEAD^","after":"HEAD","imports":["totals"],"runner":"unittest","tests":["-v","test_totals"]}
JSON
```

Adapt filenames, revisions and test arguments. `fixed` lists current test/input/
configuration files; `vary` lists implementation files to retrieve from each
commit. Include the needed local dependencies as fixed files. All paths must be
unique, canonical, project-relative regular files, without symlinks. Both groups
must be nonempty. Listed imports must resolve inside each copy. Installed pytest
is also supported; custom runners, renamed interfaces and larger snapshots may
need the native procedure above.

Requires Python 3.9+ and POSIX. Selected snapshots total at most 20 MB. Each check
defaults to 30 seconds (`--timeout`, maximum 300); output retains the last 12,000
characters. Temporary copies are project-local and cleaned afterward. Trusted
tests only: this is not a security sandbox. It checks selected original contents,
not every possible side effect. JSON includes resolved commits, fixed-file hashes
and separate check outputs/statuses. CLI exit 0 means observations were collected,
**not** that the fix was proved; setup failures still require interpretation.
