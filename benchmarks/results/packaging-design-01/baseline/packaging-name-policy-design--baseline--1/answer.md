I’ll inspect the local validation paths and run the requested filenames with the supplied Python, keeping observed behavior separate from inferred proposal effects.

**Keep the existing separation; reject this as behavior-preserving deduplication.** The parsers share normalization, but their name-validation policies differ.

Executed results below come from the supplied Python with `-B`, calling the unmodified parsers with default arguments. I verified `packaging`, `utils`, `version`, and `tags` imported from this project, and both parser code paths resolve to local `packaging/utils.py`.

| Filename | Native result observed | Proposal effect—inferred, not executed |
|---|---|---|
| `demo_pkg-1.0-py3-none-any.whl` | Name `demo-pkg`, `Version('1.0')` | Unchanged |
| `demo__pkg-1.0-py3-none-any.whl` | `packaging.utils.InvalidWheelFilename` | **Accepted** as `demo-pkg`, `Version('1.0')` |
| `éclair-1.0-py3-none-any.whl` | Name `éclair`, `Version('1.0')` | **`packaging.utils.InvalidName`** |
| `_demo-1.0-py3-none-any.whl` | Name `-demo`, `Version('1.0')` | **`packaging.utils.InvalidName`** |
| `demo-pkg-1.0.tar.gz` | Name `demo-pkg`, `Version('1.0')` | Unchanged |
| `demo__pkg-1.0.zip` | Name `demo-pkg`, `Version('1.0')` | Unchanged |
| `éclair-1.0.tar.gz` | Name `éclair`, `Version('1.0')` | **`packaging.utils.InvalidName`** |
| `-1.0.zip` | `packaging.utils.InvalidSdistFilename` | Unchanged: retained empty-name check |

All successful wheel calls also returned build `()` and a frozenset containing tag `py3-none-any`. Exceptions were caught only to record their concrete classes and messages.

The source explains these differences:

- [Wheel validation](project/packaging/utils.py#L267) rejects `__` explicitly, then uses the [Unicode wheel-name regex](project/packaging/utils.py#L77), which permits Unicode word characters and leading underscores.
- [Validated canonicalization](project/packaging/utils.py#L70) uses an ASCII core-metadata name grammar: alphanumeric endpoints, with internal `.`, `_`, and `-` allowed—including repeated underscores. Failure raises [`InvalidName`](project/packaging/utils.py#L115).
- [Sdist parsing](project/packaging/utils.py#L351) checks the separator and empty name, then normalizes without validating the name grammar. Its [documented failures](project/packaging/utils.py#L313) cover extension, separator, empty name, and version.

Thus the proposal changes both acceptance and exception contracts. `InvalidName` is a separate class from the two filename exceptions ([definitions](project/packaging/utils.py#L46)); callers catching filename-specific errors would not catch it. Static analysis also shows an empty wheel name would change from `InvalidWheelFilename` to `InvalidName`. Name validation still precedes version parsing, so newly rejected names can also change which error wins.

A viable alternative is to retain format-specific validation and keep both calls to `canonicalize_name(name_part)` unchanged. Normalization is already shared. If extraction is desired, a wheel-specific private validator could preserve the current predicate, exception class, and message; routing through core-metadata validation cannot preserve them.

For a concrete **hypothetical future policy change**, suppose core-metadata validation starts rejecting consecutive underscores. Under the proposal, `demo__pkg` would then fail in **both** consumers with `InvalidName`, before version parsing. With the current separation, the wheel continues raising `InvalidWheelFilename`, while the sdist continues returning `demo-pkg`, `Version('1.0')`. Each format can adopt that policy deliberately.

These observations establish compatibility differences, not specification violations merely because inputs are accepted. No upstream tests or historical revisions were available or run. No files were edited or scratch created; runtime before/after checks confirmed unchanged project file contents and modes, including Git metadata.
