I’ll use the con-artist skill to trace the assertions and run one isolated mutation, with a single-value control. I’ll leave the original files untouched and use the specified interpreter.


The existing assertion compares `get_list("a")` with `["123", "456"]`, so it checks both values and their order across five input forms. I’ll reverse the returned list in the disposable copy; the single-value key `b` should still return `["789"]`.


Existing coverage detects the fault. The assertion at [tests/models/test_queryparams.py:24](project/tests/models/test_queryparams.py#L24) checks the complete ordered result:

```python
assert q.get_list("a") == ["123", "456"]
```

Using the specified interpreter and con-artist’s isolated-copy helper, I ran `pytest -q tests/models/test_queryparams.py` with the repository configuration preserved.

- **Correct code:** 14 passed, exit 0.
- **One mutation:** appended `[::-1]` to `get_list`’s return expression.
- **Faulty code:** 5 failed, 9 passed, exit 1. All five input forms failed at line 24 because the result was `["456", "123"]`.
- **Single-value control:** `q.get_list("b") == ["789"]` passed on both versions.

Copied imports were verified. Original files remained unchanged, and disposable copies were removed. No additional test is needed for this demonstrated fault.
