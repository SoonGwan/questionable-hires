I’ll inspect the tests and implementation, then run an isolated mutation check with the specified interpreter. I’ll leave existing files untouched and include a single-value control.

Yes. [test_queryparams.py:24](project/tests/models/test_queryparams.py#L24) asserts:

```python
assert q.get_list("a") == ["123", "456"]
```

Exact list equality protects both completeness and order across five input forms.

In a disposable copy, I narrowly mutated `get_list` to return only the first value by appending `[:1]`.

- Correct behavior: **14 passed**.
- Mutated behavior: **5 failed, 9 passed**, all failures at that existing assertion.
- Single-value control: `q.get_list("b") == ["789"]` passed under both behaviors.

No additional test is needed. All Python/pytest commands used the specified interpreter; original source and tests remained unchanged.

[Diagnostic artifacts](commands.json) include the mutation diff, logs, and control probe.
