I’m using the con-artist skill to trace the test’s assertions and run a lost-write mutation in a disposable copy. I’ll keep all work inside this project and leave production code untouched.

The baseline passes, but the test checks only the returned `ok` flag and discards the list. I’ll remove `store.append(record)` in the disposable copy, then check whether an assertion on the list contents detects the lost write.

**The test does not catch a lost write.** `test_service.py:6` checks only `ok`, which remains `True` when `store.append(record)` is removed.

Executed with `PYTHONDONTWRITEBYTECODE=1`:

| Implementation / test | Command | Result |
|---|---|---|
| Original / existing | `python3 -m unittest -v test_service` | PASS |
| Lost-write mutation / existing | `python3 -m unittest -v test_service` | PASS |
| Original / stronger | `python3 -m unittest -v test_write_contract` | PASS |
| Lost-write mutation / stronger | `python3 -m unittest -v test_write_contract` | FAIL: `[] != ['record']` |

The smallest stronger test retains and checks the store:

```python
store = []
self.assertTrue(save(store, 'record')['ok'])
self.assertEqual(store, ['record'])
```

The mutation and stronger test ran only in a disposable copy inside this project, which was removed. Production code and the existing test remain byte-for-byte unchanged.
