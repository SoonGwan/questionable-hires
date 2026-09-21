I’ll use the con-artist skill to trace the contract through the tests, then verify coverage gaps with controlled faults and stronger assertions in disposable project copies. I’ll preserve the originals and remove all scratch files.


The existing tests check value equality for one record and `KeyError` for a missing key. They don’t check record identity, write-through edits, or separation between keys. I’ll test a fault where `get()` returns a shallow copy, then verify stronger assertions for those contract requirements.


`test_service.py` does **not** protect the complete contract. Its two tests check single-record equality and missing-key `KeyError`; neither checks identity, write-through edits, or multiple-key behavior.

The controlled fault changed only:
```python
return self.records[key]
```
to:
```python
return dict(self.records[key])
```

Both existing tests passed despite the broken identity and write-through behavior.

| Tests | Implementation | Native count | Exit |
|---|---|---:|---:|
| Existing | Correct | 2, passed | 0 |
| Existing | Faulty | 2, passed | 0 |
| Existing + stronger | Correct | 6, passed | 0 |
| Existing + identical stronger | Faulty | 6, four assertion failures | 1 |

Original identities: `test_service.Existing.test_known`, `test_service.Existing.test_missing`.

Stronger identities under `test_stronger.Stronger`:

- `test_exact_records`: `assertIs(registry.get(key), records[key])` failed for both keys.
- `test_edits_visible_on_later_get`: expected edited data; received `{'n': 1}`.
- `test_edits_visible_in_input`: original input likewise retained `{'n': 1}`.
- `test_keys_keep_own_records`: checked distinct records and cross-key isolation; passed both implementations. This fault does not demonstrate sensitivity to cross-key corruption.

Used the supplied interpreter with `-B audit_runner.py -v test_service`, then added `test_stronger`. The wrapper invoked native `unittest.main()` and verified copy-local module and method bindings inside every test process. Failures were behavioral assertions, with no setup errors.

All disposable copies were removed. Original contents, modes, Git HEAD/index, and skill resources remained unchanged.
