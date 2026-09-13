# Gather an audit slice without executing project code

When Python test/implementation paths are known but their context has not been
read, collect it once with the installed skill's read-only CLI:

```sh
python -B /path/to/con-artist/scripts/context.py --root /permitted/project \
  tests/test_service.py service.py:Store.save
```

Supply 1–8 explicit `file[:qualified.definition]` selectors. Files are returned in
full, or the selected class/function/method with decorators and original line
numbers. For their ancestor directories **inside the supplied root**, output
includes complete `AGENTS.md`/`AGENTS.override.md` contents, paths checked for
those instructions, common pytest config files, and static conftest indexes.
Follow applicable instructions; host rules determine precedence. Parent-root
instructions and additional host-configured instruction names are not discovered.

Conftest indexes retain top-level statements (including imports/plugin settings),
definition locations and decorators. Read relevant fixtures, autouse setup,
hooks/plugins and unresolved dependencies using the returned paths/line numbers.
This is navigation, **not** a resolved fixture graph or assurance that code is
safe to execute. Definition excerpts omit surrounding imports/globals/base
classes; inspect them when their semantics matter. Never execute extracted
function text as a substitute for the implementation.

Reuse collected paths/content while files remain unchanged; don't add this call
after equivalent context is already available. Then perform the actual audit
using project facilities or [the copy helper](python-audit.md) as appropriate.
Neither collector exit 0 nor a source hash is execution evidence.

Python 3.9+, UTF-8 regular files only, no imports/subprocesses/writes. Symlinks,
traversal and Git internals are refused. Maximum 256 KB per file, 2 MB total input and 100,000
output characters; invalid/oversized context exits 2 with no partial stdout.
Unsupported Python syntax in a conftest index also fails explicitly. Use native
project tools for unsupported layouts; don't install dependencies for this tool.
Files must be stable during reading; this is not a sandbox against concurrent
filesystem changes. Output includes relative paths and source hashes; it may
contain private source/configuration and is not automatically safe to publish.
