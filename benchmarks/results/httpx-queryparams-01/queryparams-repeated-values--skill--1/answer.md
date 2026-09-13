I’ll use the con-artist skill to trace the assertions, run a baseline, and check one isolated mutation with a single-value key as the control. Original source and tests will remain untouched.


The existing test asserts the exact ordered list `["123", "456"]` for five input forms. I’ll mutate `get_list` to return only the first value, then check that the assertion fails while the single-value key `b` still returns `["789"]`.


Existing coverage detects the fault; no additional test is needed.

The detecting assertion is [test_queryparams.py:24](project/tests/models/test_queryparams.py#L24):

```python
assert q.get_list("a") == ["123", "456"]
```

Exact list equality checks both values and their order across five input forms.

Using the requested interpreter and the skill’s isolated-copy helper, I ran `pytest -q tests/models/test_queryparams.py`:

- **Correct implementation:** 14 passed, exit 0.
- **Mutation:** appended `[:1]` to `get_list`’s return expression. All five parametrizations failed at that assertion: `['123'] != ['123', '456']`; 9 passed, exit 1.
- **Single-value control:** `q.get_list("b") == ["789"]` passed on both implementations, exit 0.

Copied imports were verified in the execution processes. Disposable copies were removed, and original source and tests remained unchanged.
