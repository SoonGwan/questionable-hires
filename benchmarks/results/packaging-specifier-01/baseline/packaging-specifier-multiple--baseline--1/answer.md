I’ll inspect the source and consuming tests, then run the correct code and each isolated mutation in disposable local copies. Each pytest process will verify its imports and class binding; I’ll remove all scratch files afterward.

The requested replacements affect compatible-release matching (`~=`), non-wildcard equality (`==`), and inequality (`!=`). The existing parameterized membership test has positive cases for all three. I’ll now check which assertion first detects each mutation.

All three independent mutations were detected by the original tests.

| Implementation | Native result | Exit | First detecting case |
|---|---|---|---|
| Correct | 806 passed | 0 | — |
| Compatible comparison → `False` | 376 passed, 1 failed | 1 | `test_specifiers[1-~=1.0-True]` |
| Non-wildcard equality → `False` | 311 passed, 1 failed | 1 | `test_specifiers[2.0-==2-True]` |
| Inequality → `False` | 338 passed, 1 failed | 1 | `test_specifiers[2.1-!=2-True]` |

Each failure occurred in `TestSpecifier.test_specifiers`, at `tests/test_specifiers.py:482`: `assert version in spec`. With `prereleases=True`, the respective membership checks returned `False` instead of the expected `True`.

Four actual native pytest executions used the supplied Python with `-B` and exactly:
```text
tests/test_specifiers.py -x -q --tb=short -p no:cacheprovider
```

Every process collected 806 tests and verified that `packaging` and `packaging.specifiers` loaded from its disposable copy’s `src`, and that `tests.test_specifiers.Specifier is packaging.specifiers.Specifier`. Binding checks also ran before every executed test.

Only the specified replacement was applied in each mutant copy; existing tests remained unchanged. No mutant survived, so no additional regression assertion was needed. Fail-fast proves first detection, not complete mutant-suite coverage. The correct baseline ran once.

All scratch was removed. File-content hashes and modes, including Git HEAD/index, matched before and after.
