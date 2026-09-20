I’ll inspect the revisions and current tests, then run both copies of `allocation.py` against the same test file and Python runtime. I’ll capture failures and exit codes, and remove all comparison scratch before finishing.

The change accumulates duplicate SKU quantities instead of keeping only the last quantity. The current suite has two tests for that behavior and three controls. I’ll run the native unittest command in two scratch directories, with each test process recording its revision, loaded module path, module hash, and Python runtime.

Verified: **HEAD passes all five tests; its parent fails two.**

Both ran `python3 -B -m unittest -v test_allocation` using Python **3.9.6**, executable `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`, and identical copies of the current, unchanged `test_allocation.py`.

| Test | HEAD^ | HEAD |
|---|---|---|
| `test_duplicate_lines_accumulate` | FAIL | PASS |
| `test_aggregate_shortage_is_atomic` | FAIL | PASS |
| `test_distinct_lines_control` | PASS | PASS |
| `test_empty_order_control` | PASS | PASS |
| `test_invalid_order_control` | PASS | PASS |
| **Native test process exit** | **1** | **0** |

### Fix versus controls

- **Duplicate accumulation:** parent returned `{'a': 5, 'b': 4}` instead of expected `{'a': 3, 'b': 4}`. HEAD correctly sums quantities `2 + 3` and passes the input-preservation assertion.
- **Aggregate shortage:** parent failed with `AssertionError: ValueError not raised`. HEAD rejects demand `5 + 4` against stock `8` with `"insufficient stock"` and passes the input-preservation assertion.
- **Passing controls:** both handle distinct SKUs, return an equal but separate mapping for empty orders, and reject zero, negative, and unknown-SKU orders.

### Revision and import evidence

Each native test process recorded its loaded `allocation.__file__`, `reserve.__code__.co_filename`, and SHA-256 matching the corresponding Git copy.

Paths below are relative to the project:

| Version | Full revision | Copied module |
|---|---|---|
| HEAD^ | `d4e02e4ef3a633cc2ea6070fea6edcc713b89be5` | `.allocation-verification-1kf4da4a/parent/allocation.py` |
| HEAD | `794c3f550bfe28216384b6d12c4f9dd10e3648ce` | `.allocation-verification-1kf4da4a/head/allocation.py` |

All scratch was removed. The final snapshot confirmed original paths, file contents, and modes were preserved. No report or harness remains.
