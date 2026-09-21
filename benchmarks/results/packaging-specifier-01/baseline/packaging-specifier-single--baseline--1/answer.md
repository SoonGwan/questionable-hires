I’ll inspect the source and tests, then run the unchanged test file on correct and mutated disposable copies, verifying imports and class binding inside each pytest process.

The original tests **detect the requested mutation** in `_compare_compatible`.

| Implementation | Collected | Native result | Exit |
|---|---:|---|---:|
| Correct | 806 | 806 passed | 0 |
| Exact `return False` replacement | 806 | 376 passed, 1 failed | 1 |

First detection: `tests/test_specifiers.py::TestSpecifier::test_specifiers[1-~=1.0-True]`, line 482:

```python
assert version in spec
```

Here, `version == "1"` and `spec == Specifier("~=1.0", prereleases=True)`. Membership should be `True`; the mutant returns `False`.

Both executions used the supplied Python with `-B`, copy-local `src`, and native `pytest.main` with exactly:
`tests/test_specifiers.py -x -q --tb=short -p no:cacheprovider`.

Inside each actual pytest process, assertions verified copy-local `packaging` and `packaging.specifiers` paths, the copied test module path, and `tests.test_specifiers.Specifier is packaging.specifiers.Specifier`.

These were two fresh executions, with no result reuse. Fail-fast establishes first detection only; subsequent mutant cases remain untested. No additional regression was needed.

All scratch was removed. Original file contents and modes, including Git metadata, remained unchanged.
