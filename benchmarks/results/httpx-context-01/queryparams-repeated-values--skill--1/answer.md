I’ll use the con-artist skill to trace the assertions, run a baseline, and check one isolated mutation with a single-value control. I’ll leave the original source and tests unchanged.

The existing test compares the full result to `["123", "456"]`, so it checks both values and their order across five input forms. I’ll mutate `get_list` to return only the first value and verify that the single-value key `b` still returns `["789"]`.

Existing coverage detects the fault. The assertion at [test_queryparams.py:24](project/tests/models/test_queryparams.py#L24) checks both completeness and order:

```python
assert q.get_list("a") == ["123", "456"]
```

One isolated mutation appended `[:1]` to `get_list`’s return value.

- Baseline: **14 passed**, exit 0.
- Mutant: **5 failed, 9 passed**, exit 1. All five input forms failed at that assertion: `['123'] != ['123', '456']`.
- Single-value control: `q.get_list("b") == ["789"]` passed on both versions.

Used the specified interpreter and audit helper to run `pytest -q tests/models/test_queryparams.py`, preserving project configuration and verifying copied imports. Disposable copies were removed; original files remained unchanged. No additional test is needed for this fault.
