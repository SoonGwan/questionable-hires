I’m using the con-artist skill to trace the contract and test assertions, then verify any coverage gap in disposable project copies.


The existing tests check value equality for one key and `KeyError` on an empty registry. They don’t check record identity, shared edits, or separation between keys. I’ll test a narrow fault that returns a copy of each record, then verify stronger assertions for those contract requirements.


`test_service.py` does **not** protect the complete contract. Its equality assertion accepts copied records; it never checks identity, shared edits, or multiple keys.

The isolated fault changed `get()` to `return dict(self.records[key])`.

| Tests | Correct implementation | Faulty implementation |
|---|---|---|
| Original, unchanged | 2 tests, exit 0 | 2 tests, exit 0 |
| Original + identical stronger tests | 6 tests, exit 0 | 6 tests, exit 1 |

Original identities: `test_service.Existing.test_known` and `test_missing`.

Stronger identities under `test_contract.Contract`:

- `test_exact_supplied_record`: `assertIs(registry.get("a"), record)`.
- `test_returned_edits_remain_visible`: checks changed and added fields through later gets and the original input.
- `test_different_keys_retain_their_records`: checks each key’s object identity and that editing one leaves the other unchanged.
- `test_missing_key_in_populated_registry`: checks `KeyError` with existing records.

The mutant produced six assertion failures, including subtests: equal records were different objects, and both edit destinations retained `{"n": 1}`. These were behavioral failures, not setup errors.

All runs used the supplied interpreter with `-B`, invoking native `unittest` through `runpy` after asserting copy-local module and method-code paths in the same process.

All original bytes and modes, Git state, and skill resources were preserved. Disposable copies were removed; no changes were applied.
