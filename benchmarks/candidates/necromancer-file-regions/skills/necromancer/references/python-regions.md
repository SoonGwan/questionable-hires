# Named Python excerpts

Use when the current or historical source path and relevant function names are
already known. A short native source read needs no helper. For a current file:

```sh
python3 /actual/skill/path/scripts/python_regions.py --path src/module.py --name Class.method --name other_function
```

`--path` reads at most2,000,001 bytes from the supplied file and does not execute
its code. The original2MB limit still applies. `input_path` records the supplied
path; hashes identify the bytes read, not Git identity, runtime binding or an
atomic filesystem snapshot. File access/encoding/syntax errors exit2. The caller
owns permitted paths and a process deadline; file access can block. Without
`--path`, stdin behavior and report schema remain unchanged. For history:

```sh
set -o pipefail
git show '<revision>:<historical-path>' | python3 /actual/skill/path/scripts/python_regions.py --name Class.method --name other_function
```

Check the Git producer's errors and the pipeline status. The source SHA-256
identifies stdin bytes, **not** their revision or provenance. Use verified local
history; the helper does not fetch anything or run Git. Python 3.9+ is required,
and the input must be valid syntax for the selected interpreter.
An optional leading UTF-8 BOM is accepted and omitted from excerpt text; byte
counts and source hashes still identify the original input including the BOM.

Compact JSON retains original indentation, decorators, physical line numbers and
top-level future-import feature names. Parenthesized or explicitly continued
decorators retain their opening `@` line, not merely the expression location
recorded by the AST. Bare names retain every matching scope;
dotted names narrow the scope but still retain duplicate definitions (for example
property accessors or conditional definitions). It does not resolve runtime
binding. `complete` means requested definitions were found without text truncation,
not that all relevant context was collected. Inspect dependencies, callers and
surrounding changes when they matter; do not transplant excerpts as executable
replacements without preserving their original bindings/compiler context.

Limits: 2 MB UTF-8 input, 1–10 names, at most 20 matching definitions and 12,000
characters of region text shared across matches. Missing names and truncated
regions produce `complete: false` and exit 1; invalid/unsupported input exits 2.
Later matches can have empty truncated text after the shared budget is exhausted.
Excerpt text is sliced only up to the remaining allowance, using physical-line
offsets rather than first copying complete overlapping bodies. Definitions and
match limits are still checked after text space is exhausted; metadata is retained.
Discovery traverses statement containers, including exception handlers and match
cases, but skips expression subtrees, which cannot contain function statements.
Use a narrower selection or a focused source read rather than treating omissions
as absence. No input code is executed or source files written; AST parsing is not
a sandbox or a total-memory guarantee. This helper's effect on whole-task model
cost has not yet been measured.
