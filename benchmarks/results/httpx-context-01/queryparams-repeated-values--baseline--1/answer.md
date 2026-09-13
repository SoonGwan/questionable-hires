I’ll inspect the existing coverage, then run it against an isolated mutation that drops repeated values while preserving a single-value control. All disposable files will stay inside this project.

Existing coverage protects both values and their order: [test_queryparams.py:24](project/tests/models/test_queryparams.py#L24) asserts:

```python
assert q.get_list("a") == ["123", "456"]
```

In a disposable copy, I changed only `get_list`’s return expression to `list(self._dict.get(str(key), []))[:1]`.

- Correct behavior: **14 passed**.
- Mutated behavior: **5 failed, 9 passed**; all five input variants failed at that assertion.
- Single-value control: `get_list("b") == ["789"]` passed in both versions.

No additional test is needed. All Python/pytest commands used the specified interpreter. Original files were verified unchanged; copies, mutation diff, and logs remain in `queryparams-audit-tb29g1bp/`.
