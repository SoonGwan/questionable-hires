# Receipt for a fix that already exists

Reuse valid existing evidence. Otherwise freeze the current regression assertion
and inputs in isolated copies; vary implementation, **not each revision's tests**.
Keep dependencies/configuration comparable and identify the loaded revisions.
An old-interface/setup failure is not reproduction: disclose incompatibility
instead of substituting a different check. The entrypoint's runtime, scope,
exit-status and stopping rules still apply; do not install missing dependencies.

## Optional Python comparison helper

For small local Python comparisons, the installed helper handles copying,
import provenance and cleanup. Invoke it without reading its source unless
adaptation is needed. Adapt this recipe to actual files, commits and test arguments:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --python /path/to/project/python --spec - <<'JSON'
{"fixed":["test_parser.py"],"vary":["parser.py"],"before":"HEAD^","after":"HEAD","imports":["parser"],"runner":"unittest","tests":["-v","test_parser"]}
JSON
```

`fixed`: current tests, inputs, configuration and required local dependencies.
`vary`: implementation files from each commit. Both lists are nonempty, disjoint,
canonical project-relative regular files; no symlinks. Listed imports must resolve
inside each copy. Use the project interpreter and unittest or installed pytest;
other runtimes/custom runners require native isolated comparison instead.

Python 3.9+, POSIX; 20 MB snapshot budget, 30 seconds/check (`--timeout` up to 300),
last 12,000 output characters. Project-local copies are cleaned; selected original
contents are checked, not every side effect. Trusted tests only, **not a sandbox**.
JSON records revisions, fixed-file hashes and separate outputs/statuses. CLI exit
0 means collected observations, **not proof**: inspect the assertion failure,
after pass and provenance before claiming the fix.
