I’ll use the con-artist skill to compare the tests with CONTRACT.md, then check a narrow behavioral fault and any stronger assertions in disposable project-local copies. I’ll preserve the originals and remove all scratch files.


The nonempty test checks only the JSON keys, so it misses incorrect IDs and counts. The empty-list test checks the full result. I’ll reverse the returned IDs as a narrow fault, then verify stronger assertions for the full response, including order and duplicates.


`test_service.py` does **not** protect the complete contract. `Existing.test_nonempty` checks only keys, missing ID values, order, duplicates and count. Neither original test explicitly requires a string return.

The narrow fault changed `list(items)` to `list(reversed(items))`.

All four processes ran `python3 -B -m unittest -v test_service`:

| Tests | Implementation | Native result | Exit |
|---|---|---|---|
| Original | Correct | 2 passed | 0 |
| Original | Reversed IDs | 2 passed | 0 |
| Stronger | Correct | 2 passed | 0 |
| Identical stronger | Reversed IDs | 2 tests; 2 subtest failures | 1 |

Both versions used `test_service.Existing.test_empty` and `test_service.Existing.test_nonempty`. The stronger version checks string output, integer types and exact decoded responses for empty, duplicate-containing, zero and large-ID inputs. Its decisive assertion was:

```python
self.assertEqual(decoded, {"ids": items, "count": len(items)})
```

For `[4, 4, 2]`, it correctly rejected `[2, 4, 4]`. This verifies detection of the order fault; the other identified gaps were established by assertion inspection.

Copy-local implementation bindings were confirmed inside every test process. All original bytes/modes, Git metadata and skill resources remained unchanged; all owned scratch was removed.
