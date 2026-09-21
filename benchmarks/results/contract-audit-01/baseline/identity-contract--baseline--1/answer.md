I’ll compare the tests with the contract, then use disposable project copies to test a narrow behavioral fault and any stronger assertions needed. I’ll leave the originals unchanged.


The existing tests check value equality for one record and `KeyError` for an empty registry. They don’t check record identity, mutation visibility, or behavior across keys. I’ll test a narrow fault that returns a shallow copy of each record, then run the same stronger assertions against both implementations.


`test_service.py` does **not** protect the complete contract. It checks one record’s value equality and a missing key in an empty registry, but omits object identity, mutation visibility, and multiple-key behavior.

The disposable faulty implementation changed only:
```python
return dict(self.records[key])
```
This returns an equal copy, violating the required identity and shared mutation behavior.

Using the supplied interpreter with `-B -m unittest -v`:

| Tests | Correct implementation | Faulty implementation |
|---|---|---|
| Unchanged existing suite | 2 passed; exit 0 | 2 passed; exit 0 |
| Identical stronger suite | 4 passed; exit 0 | 3 failed, 1 passed; exit 1 |

Original test identities: `test_service.Existing.test_known` and `test_missing`.

Stronger identities under `test_stronger.Stronger`:

- `test_exact_supplied_objects`: asserts identity with supplied records, including empty records and shared aliases.
- `test_returned_edits_visible_everywhere`: checks updates, additions, and deletion through later gets and the original input.
- `test_keys_keep_their_own_records`: checks separate keys retain their records.
- `test_missing_in_populated_registry`: checks `KeyError` with existing records.

Decisive failures were `assertIs(...)` rejecting equal copies and a later get returning `{'n': 1, 'remove': True}` instead of the edited `{'n': 7, 'added': 'visible'}`. These were behavioral assertion failures.

Each native process verified copy-local module paths, method code binding, and test-module references. Original contents and modes, including Git metadata, were preserved. All disposable files were removed.
