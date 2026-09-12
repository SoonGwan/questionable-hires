I’ll use the con-artist skill to test each fault in isolation, then verify stronger assertions if needed. I’ll leave the original files unchanged and remove the temporary audit workspace.

Both faults survive the existing test: it checks only the truthiness of the return value and never examines the store.

I ran separate disposable copies of the actual implementation, verifying that the existing test imported each copied `save`.

| Implementation | Existing test | Stronger test |
|---|---|---|
| Correct, unchanged | PASS (exit 0) | PASS (exit 0) |
| Lost write: remove `store.append(record)` | PASS (exit 0) | FAIL (exit 1): missing `'new'` |
| Duplicate write: repeat `store.append(record)` | PASS (exit 0) | FAIL (exit 1): extra `'new'` |

Commands executed:
```sh
python3 -B -m unittest -v test_service
python3 -B -m unittest -v test_contract
```
The first also passed in the original project. Both commands ran separately in each isolated variant.

The temporary stronger test used:
```python
store = ['old-first', 'old-second']
self.assertIs(save(store, 'new'), True)
self.assertEqual(store, ['old-first', 'old-second', 'new'])
```
The full-list assertion checks exactly one appended record and preservation of pre-existing records in order. Both faulty variants failed at this assertion.

Original source, tests, and README were verified byte-for-byte unchanged. All temporary audit files were removed. No dependencies were installed or external services used.
