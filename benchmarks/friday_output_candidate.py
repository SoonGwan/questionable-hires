"""Unadopted guide-only output candidate based on resource 75f6b4f."""
RESOURCE = '75f6b4f'
ORIGINAL = '''with recipe JSON on stdin (or a recipe path instead of `-`). For value assertions,
use the same recipe through the API and reuse its result:

```python
import runpy
helper = runpy.run_path('<skill-dir>/scripts/sqlite_matrix.py')
matrix, format_result = helper['matrix'], helper['format_result']
result = matrix(recipe, project_root, timeout=5)
print(format_result(result))
```

Rows retain tuples/BLOB bytes; `format_result` encodes JSON without rerunning SQL
or changing the result. Inspect implementation only for trust/adaptation/troubleshooting.'''
CANDIDATE = '''with recipe JSON on stdin (or a recipe path instead of `-`). For contract checks,
collect once through the API, then assert the required observations below:

```python
import runpy
helper = runpy.run_path('<skill-dir>/scripts/sqlite_matrix.py')
result = helper['matrix'](recipe, project_root, timeout=5)
```

Keep native rows/BLOB bytes in `result`. After assertions, print identified
phase/check outcomes and decisive mismatches, not automatically the entire matrix
as well. Preserve failure details, incomplete/unrun checks and required provenance;
a success label alone is not evidence. Use `helper['format_result'](result)` for
requested raw observations or unresolved diagnostics; it serializes without reruns.
Inspect implementation only for trust/adaptation/troubleshooting.'''


def revise(guide):
    if guide.count(ORIGINAL) != 1 or CANDIDATE in guide:
        raise ValueError('Expected exactly one original API example')
    return guide.replace(ORIGINAL, CANDIDATE)
