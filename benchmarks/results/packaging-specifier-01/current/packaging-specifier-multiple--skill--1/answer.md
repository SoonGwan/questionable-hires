I’ll use the con-artist skill to inspect the source and tests, then run the baseline and each isolated mutation in disposable project-local copies with same-process import checks.

The tests exercise all three operators through `version in spec`, which calls `contains()` and dispatches to the comparison method. Each operator has positive membership cases. I’ll now check whether the requested mutations fail those assertions in native pytest.

All three independent mutations were detected by the original tests.

Used the supplied Python 3.11.16 with `-B` and native `pytest.main()` with exactly:
```text
tests/test_specifiers.py -x -q --tb=short -p no:cacheprovider
```

Each run collected **806 tests**:

| Implementation | Native result | Exit | First detecting case |
|---|---:|---:|---|
| Correct | 806 passed | 0 | — |
| Compatible comparison → `False` | 376 passed, 1 failed | 1 | `test_specifiers[1-~=1.0-True]` |
| Exact equality → `False` | 311 passed, 1 failed | 1 | `test_specifiers[2.0-==2-True]` |
| Inequality → `False` | 338 passed, 1 failed | 1 | `test_specifiers[2.1-!=2-True]` |

Every detection occurred at `tests/test_specifiers.py:482`, `assert version in spec`: expected membership was `True`, but the mutant returned `False`. Source inspection confirmed the path through `__contains__`, `contains`, and operator dispatch.

Within each actual pytest process, collection and per-test checks verified copy-local `packaging` and `packaging.specifiers` paths, plus `tests.test_specifiers.Specifier is packaging.specifiers.Specifier`.

Four executions used separate disposable copies with unchanged tests and only the exact requested replacement per mutant. The single correct baseline served all three comparisons; it was not rerun. No mutant survived, so no additional regression assertion was needed. Fail-fast establishes first detection only.

Scratch was removed. Final inventory confirmed unchanged project contents and modes, including supplied source/tests/licenses, Git metadata, and skill resources. No permanent harness or report remains.
