# Gather an audit slice without executing project code

When Python test/implementation paths are known but their context has not been
read, collect the relevant slice once with the installed skill's read-only CLI.
A suite selected for execution is not automatically a whole-file reading list.
For known assertions, select their definitions; use a targeted project search to
locate unknown ones. For a file whose whole assertion context is needed:

```sh
python -B /path/to/con-artist/scripts/context.py --root /permitted/project --full \
  tests/test_service.py service.py:Store.save
```

This reads the test body and only `Store.save` from the implementation in one
call. CLI output is compact JSON; `--pretty` restores indentation for manual
inspection without changing fields or source text. Omit `--full` for a locating pass when needed definitions are unknown;
do not request an index first when you already need the file's assertions.
For a very large test file, select the relevant test definitions and inspect
their unresolved setup instead of forcing a whole-file read past output limits.

Supply 1–8 explicit `file[:qualified.definition]` or `file:line` selectors. A
positive line number from a traceback (for example, `service.py:42`) selects
the smallest enclosing Python definition, including decorators, and reports
`requested_line` plus its static qualified name. Nested/conditional definitions
are supported; names do not prove runtime bindings. Out-of-range lines and
module-level lines outside a definition fail explicitly: select the full file
for that context. `--full` does not override explicit line selection.

When the requested
definition is known, select it directly (`service.py:Store.save`) rather than the
whole implementation file. It includes decorators and original line numbers.
Named selection follows static definitions through control-flow blocks without
evaluating conditions, and respects class/function scopes. Multiple definitions
at any selected scope are ambiguous, including an unconditional definition plus
a conditional replacement; use an explicit line or inspect the enclosing source.
A unique static definition does not prove that its branch executes or that a later
assignment/decorator preserves its runtime binding. Index coverage is unchanged;
conditional class-body definitions may require surrounding source inspection.
Line numbers follow Python physical lines (LF, CRLF or CR). Unicode separators
and control characters inside literals do not create extra source lines. Excerpts
use LF between numbered lines; hashes still identify the original file bytes.
Unqualified Python files over 200 lines return a definition/method index when
that is smaller than full source; smaller files remain complete. Output labels
`representation` and `bodies_omitted` explicitly. Read the needed bodies using
the returned line ranges; an index is not reviewed source. `--full` restores full
selected files when needed, subject to the same size limits. It does not expand
ancestor conftest indexes or override an explicit definition selector.

For selected-path ancestor directories **inside the supplied root**, output
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

Within one invocation, selectors and ancestor context reuse one read and at most
one parse per relative file path; the input limit counts that file once.
Multiple line selectors also reuse one definition-span traversal for that parsed
file. Each still resolves the smallest enclosing definition and rejects ambiguity;
named selectors do not build this line index. Named selectors reuse a name map
per visited statement scope, retaining all duplicate definitions for ambiguity
checks. Nothing is cached across invocations.
Definition discovery skips expression subtrees, which cannot contain definition
statements; deep arithmetic/decorator expressions therefore do not consume its
recursive walk budget. Parsing and nested statement scopes still have runtime limits.
Decorator indexing shares physical UTF-8 lines across definitions instead of
rescanning the whole file for each decorator; original decorator text is retained.
Output still retains each requested excerpt and its provenance. No cache survives the
invocation, and different files are not an atomic filesystem snapshot.

Reuse collected paths/content while files remain unchanged; don't add this call
after equivalent context is already available. Then perform the actual audit
using project facilities or [the copy helper](python-audit.md) as appropriate.
Neither collector exit 0 nor a source hash is execution evidence.

Python 3.9+, UTF-8 regular files only, no imports/subprocesses/writes. Symlinks,
traversal and Git internals are refused. Maximum 256 KB per file, 2 MB total input and 100,000
output characters; invalid/oversized context exits 2 with no partial stdout.
Unsupported Python syntax in an indexed file also fails explicitly (`--full`
can read a selected file without parsing it). Use native
project tools for unsupported layouts; don't install dependencies for this tool.
Files must be stable during reading; this is not a sandbox against concurrent
filesystem changes. The opened file's type and identity are checked against the
inspected path before reading; where available, nonblocking/no-follow open flags
reject a replaced FIFO or symlink without reading it. This is not an atomic
snapshot or protection against parent-directory races or writes to the same file.
Output includes relative paths and source hashes; it may
contain private source/configuration and is not automatically safe to publish.
