I’ll use the con-artist skill to trace the test’s write path, run an isolated missing-append mutation, and verify whether a stored-record assertion detects it while preserving an existing record.


The test **does not catch a lost write**: it asserts only `result['ok']`.

Using `python3 -B .agents/skills/con-artist/scripts/audit.py --spec -`, I removed only `store.append(record)` in disposable project-local copies.

| Check | Correct code | Missing append |
|---|---|---|
| Existing `unittest -v test_service` | Pass (0) | Pass (0) |
| Stronger stored-record assertion | Pass (0) | Fail (1) |

The identical stronger probe started with `['existing']`, saved `'record'`, and asserted:

```python
assert store == ['existing', 'record']
```

Faulty code retained only `['existing']`, producing the intended assertion failure.

Each execution verified that the actual test’s global `save` was the copied `service.save`, including its implementation path. Original files remain unchanged, user changes were preserved, and owned disposable copies were removed.
