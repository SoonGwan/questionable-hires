I’ll inspect the existing assertions, then run a narrow mutation in a disposable copy inside the project, leaving the original files untouched.

Existing coverage protects both values and their order. The detecting assertion is [test_queryparams.py:24](project/tests/models/test_queryparams.py#L24):

```python
assert q.get_list("a") == ["123", "456"]
```

One isolated mutation reversed `get_list`’s returned list:

- Correct copy: **14 passed**.
- Mutated copy: **5 failed, 9 passed**, all failures at that assertion.
- Single-value control: `q.get_list("b") == ["789"]` passed in both copies.

No additional test is needed. All Python commands used the specified interpreter. Original source and tests remain unchanged; copies, mutation diff, and diagnostic logs are in `queryparams-audit/`.
