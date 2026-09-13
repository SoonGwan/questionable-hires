I’ll use the con-artist skill to trace both contracts, run each fault in a separate disposable copy, and check the lowercase control against all three versions. I’ll leave the existing source and tests untouched.

The tests directly assert uppercase lookup and ordered `get_list` results, including an unsplit comma-containing value. I’ll remove lookup lowercasing for the first fault and reverse the default `get_list` result for the second. Both changes should preserve the lowercase single-value control.

Both selected faults were **killed by existing assertions**.

| Isolated mutation | Result | Detecting assertion |
|---|---|---|
| Remove `.lower()` from `__getitem__` lookup normalization | 1 failed, 26 passed | `tests/models/test_headers.py:31`: `assert h["A"] == "123"` raises `KeyError('A')`. |
| Reverse values returned by `get_list` when `split_commas=False` | 2 failed, 25 passed | Line 16 expects `["123", "456"]`; line 163 expects `["a, b", "c"]`. Both receive reversed lists. The latter also explicitly checks that commas remain unsplit by default. |

The correct-code baseline passed all **27 tests**, using the audit helper with the specified interpreter and pytest arguments `-q tests/models/test_headers.py`. Each fault ran in a separate project-local copy with verified copied imports.

This lowercase single-value control passed against correct code and each fault:

```python
h = httpx.Headers({"x-control": "ordinary"})
assert h["x-control"] == "ordinary"
assert h.get_list("x-control") == ["ordinary"]
```

No stronger assertions are needed for these detected faults. Existing files remained unchanged, and disposable copies were removed.
