I’ll inspect the existing assertions, then test each fault in a separate disposable copy with a lowercase single-value control. I’ll leave the original files unchanged.

The file already checks uppercase `__getitem__` lookup and ordered `get_list` results, including an embedded comma with `split_commas` omitted. I’ll remove lookup lowercasing for one fault and reverse values only in the unsplit `get_list` branch for the other.

Both selected faults are **detected by existing assertions**. Correct code passes all 27 tests.

| Isolated mutation | Detecting existing assertion | Result |
|---|---|---|
| Remove `.lower()` from `__getitem__` key normalization | [Line 31](project/tests/models/test_headers.py#L31): `assert h["A"] == "123"` raises `KeyError: 'A'` | 1 failed, 26 passed |
| Reverse `get_list` values only when `split_commas=False` | [Line 16](project/tests/models/test_headers.py#L16): expects `["123", "456"]`; receives `["456", "123"]`. [Line 163](project/tests/models/test_headers.py#L163) also fails. | 2 failed, 25 passed |

Line 163 calls `get_list("Set-Cookie")` without specifying `split_commas` and expects `["a, b", "c"]`, explicitly checking repeated values in order while retaining the embedded comma.

The lowercase single-value control—`Headers({"x-control": "plain"})`, checking both indexing and default `get_list`—passes on correct code and both faults.

No stronger assertions are needed for these detected faults. All commands used the specified interpreter; 125 original files were verified unchanged. Disposable copies, patches, and logs are in [headers-audit](commands.json), with execution details in [results.json](project/headers-audit/results.json).
