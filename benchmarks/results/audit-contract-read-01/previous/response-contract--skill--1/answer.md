I’ll use the con-artist skill to trace the contract assertions and test a narrow behavioral fault in disposable project copies, preserving the originals.

The empty-list test checks the complete result. The nonempty test checks only the key names, leaving ID values, order, duplicates, and count unchecked. I’ll test a fault that sorts and deduplicates IDs, then verify assertions comparing the full decoded result on empty and nonempty inputs.

`test_service.py` does **not** protect the complete contract.

- `test_service.Existing.test_empty` checks the full empty result.
- `test_service.Existing.test_nonempty` checks only key names—not ID values, order, duplicates, or count.
- Neither explicitly requires a string return value.

A copy-only mutation added `items = sorted(set(items))`. For `[4, 4, 2]`, it returned `{"ids": [2, 4], "count": 2}`. Both original tests still passed.

Using Python 3.11’s native `-B -m unittest -v` runner:

| Tests | Implementation | Native count | Exit |
|---|---|---:|---:|
| Original | Correct | 2 passed | 0 |
| Original | Faulty | 2 passed | 0 |
| Original + stronger | Correct | 3 passed | 0 |
| Original + stronger | Faulty | 3 run; 3 subtest failures | 1 |

The identical stronger test, `test_contract_stronger.Contract.test_supported_lists`, exercised six inputs covering empty lists, zero, singletons, ordering, duplicates, and large IDs. Its assertions were:

```python
self.assertIsInstance(result, str)
self.assertEqual(
    json.loads(result),
    {"ids": items, "count": len(items)},
)
```

The equality assertion detected actual ordering, duplicate, and count violations. It permits unspecified whitespace and key order.

Each native test process verified its copy-local implementation binding. All disposable copies were removed; original contents, modes, Git HEAD/index, and skill resources were verified unchanged.
