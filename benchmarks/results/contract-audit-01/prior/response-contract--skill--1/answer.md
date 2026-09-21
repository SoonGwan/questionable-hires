I’ll use the con-artist skill to trace the contract against the tests, then check any gaps with controlled faults and stronger assertions in disposable project-local copies. I’ll preserve the originals and verify which implementation each test process loads.


The nonempty test checks only the JSON keys, so it would accept lost IDs and an incorrect count. The empty test checks the full payload. I’ll test a fault that discards every input ID, then verify stronger assertions for exact values, order, duplicates, and the required JSON string return type.


`test_service.py` does **not** protect the complete contract.

- `test_service.Existing.test_nonempty` checks only the keys. ID values, order, duplicates, and count are unchecked.
- `test_service.Existing.test_empty` checks the complete empty payload.
- Neither explicitly requires a string; `json.loads` also accepts bytes.

A single controlled fault changed `render` to always serialize `{"ids": [], "count": 0}`. Both unchanged tests passed despite losing every nonempty input.

| Tests | Correct implementation | Faulty implementation |
|---|---|---|
| Original | 2 tests, exit 0 | 2 tests, exit 0 |
| Original + stronger | 3 tests, exit 0 | 3 tests, 4 subtest failures, exit 1 |

The identical stronger test, `test_contract.Contract.test_supported_examples`, covered empty input, zero, duplicates, unsorted IDs, and large integers. It required a string, exact decoded payload, and integer values. The decisive assertion was:

```python
self.assertEqual(payload, {"ids": items, "count": len(items)})
```

For `[4, 4, 2]`, it correctly rejected `{"ids": [], "count": 0}`.

All four processes used the supplied interpreter with `-B`, through a binding-check wrapper invoking native `unittest.main(module=None)`:

```text
python -B audit_runner.py -v test_service
python -B audit_runner.py -v test_service test_contract
```

Each process verified the copied module path, function source path, and tests’ actual implementation binding. Original tests remained byte-identical; stronger tests were identical across implementations.

These checks demonstrate the behavioral gap and its detection, not exhaustive correctness for every possible input. All scratch was removed. Original contents and modes, Git HEAD/index, and skill resources were preserved.
