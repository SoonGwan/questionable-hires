# Named Python excerpts

Use only when the historical revision, path and relevant function names are
already known. A short native source read needs no helper. To select functions
from a large Python module without executing its code:

```sh
set -o pipefail
git show '<revision>:<historical-path>' | python3 /actual/skill/path/scripts/python_regions.py --name Class.method --name other_function
```

Check the Git producer's errors and the pipeline status. The source SHA-256
identifies stdin bytes, **not** their revision or provenance. Use verified local
history; the helper does not fetch anything or run Git. Python 3.9+ is required,
and the input must be valid syntax for the selected interpreter.

Compact JSON retains original indentation, decorators, physical line numbers and
top-level future-import feature names. Bare names retain every matching scope;
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
Use a narrower selection or a focused source read rather than treating omissions
as absence. No input code is executed or source files written; AST parsing is not
a sandbox or a total-memory guarantee. This helper's effect on whole-task model
cost has not yet been measured.
