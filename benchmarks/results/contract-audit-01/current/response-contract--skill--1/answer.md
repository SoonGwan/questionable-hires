I’m using the con-artist skill to trace the contract coverage, then test a focused behavioral fault and stronger assertions in disposable project-local copies. I’ll preserve the originals and remove the scratch files.


The nonempty test checks only the JSON keys; it never checks the returned IDs or count. The empty test checks the full result. I’ll test a mutation that sorts and deduplicates the returned IDs, then verify stronger assertions for values, order, duplicates, count, and the supported input cases.


`test_service.py` does **not** protect the complete contract. `Existing.test_nonempty` checks only keys, leaving ID values, order, duplicates, and count unchecked. Neither existing test explicitly requires a string return.

A single mutation, `list(items)` → `sorted(set(items))`, returned `{"ids": [2, 4], "count": 3}` for `[4, 4, 2]`. Both unchanged tests passed.

| Tests | Implementation | Native count | Exit |
|---|---|---:|---:|
| Original | Correct | 2, pass | 0 |
| Original | Faulty | 2, pass | 0 |
| Stronger | Correct | 3, pass | 0 |
| Stronger | Faulty | 3, four assertion failures | 1 |

The decisive stronger assertion was:

```python
self.assertEqual(
    json.loads(service.render([4, 4, 2])),
    {"ids": [4, 4, 2], "count": 3},
)
```

Stronger tests also checked string output, integer types, and exact decoded results for empty, singleton, zero, repeated, unordered, and large IDs. They impose no whitespace or mapping-key-order requirements.

Original identities: `Existing.test_empty`, `Existing.test_nonempty`. Stronger identities: those two, with the nonempty assertion strengthened, plus `Existing.test_supported_cases`. SHA-256:

```text
Original: 94213c274a97f8aa1261f63b26a941118bd94ecfd7bf95b9606c45bc1ea5457c
Stronger: 177c567cb5ddbd9b131a89fdff12c183b03b5e7b5684ef953378f9ba1891580e
```

Each run used the supplied interpreter with `-B -m unittest -v audit_binding`. The loader verified copy-local module paths, function source binding, and test-module binding inside each test process.

All scratch copies were removed. Original contents/modes, Git HEAD/index, and skill resources were verified unchanged.
