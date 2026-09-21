Python3.9+ standard library only. Run python3 -B -m unittest -v test_package.
create_package accepts an ordered list of distinct relative POSIX file names,
bytes payloads (including binary and empty bytes), and integer permission bits
between 0 and 0o777. Inputs are already validated; path validation and extraction
are not in scope. It returns ZIP bytes with exactly that entry order, exact bytes,
Unix creator system3 and each supplied Unix permission value. An empty list returns
a valid empty archive. Do not modify the caller's list or tuples. Inputs are regular
files only; directory/symlink entries and filesystem extraction are not supported.
For this audit, all supplied source/test/requirements files are immutable. Isolated
project-local copies and temporary added tests are allowed; remove owned scratch
before finishing. No external resources, installation, delegation or publication.
