I’m using the receipt skill to compare both committed versions in isolation, run the same five tests on each, and capture failures and exits without changing production files.

Verified: the committed fix accumulates duplicate quantities instead of overwriting them.

| Version | Full revision | Native suite result | Process exit |
|---|---|---|---|
| HEAD^ | `d4e02e4ef3a633cc2ea6070fea6edcc713b89be5` | 5 tests, 2 failures | `1` |
| HEAD | `794c3f550bfe28216384b6d12c4f9dd10e3648ce` | 5 tests, all pass | `0` |

**Observed behavior**

- Duplicate lines: parent returned `{'a': 5, 'b': 4}` instead of `{'a': 3, 'b': 4}`. HEAD passes, including the unchanged-input assertion.
- Aggregate shortage: parent failed with `AssertionError: ValueError not raised`. HEAD rejects the combined request of 9 against stock of 8 with `"insufficient stock"` and preserves input.
- Passing controls on both: distinct SKUs, empty orders returning a separate mapping, and invalid quantities/unknown SKUs.

**Execution identity**

Both ran the unchanged current `test_allocation.py` using:
```text
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B -m unittest -v test_allocation
```

Each native process verified its copied `allocation` import. Copy paths, relative to the project, were:

- Parent: `.receipt-dg648kx_/before/allocation.py`
- HEAD: `.receipt-dg648kx_/after/allocation.py`

Only `allocation.py` varied. Neither run timed out or truncated output.

The project preservation guard passed, including file bytes/modes and Git metadata. Scratch copies were removed; no report or harness remains. Final diff checks exited `0`; existing untracked skill resources were preserved.
