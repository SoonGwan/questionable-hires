I’ll inspect the revisions and current tests, then run both allocation versions in isolated project scratch directories with the same test file and Python runtime. I’ll capture each run’s results and exit code, then remove the scratch files.

The change makes duplicate SKU quantities accumulate instead of overwriting earlier quantities. The existing comparison helper runs all five current tests against isolated copies and records their import paths and exit codes. I’ll use it and check that it preserves the project files and removes its scratch copies.

Verified: **HEAD passes all five tests; its parent fails two.**

Both native unittest processes used Python **3.9.6**, executable `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`, and identical, unchanged current `test_allocation.py`. Only the copied `allocation.py` differed.

| Version | Full revision | Tests | Process exit |
|---|---|---|---|
| HEAD^ | `481a3ccb54d84d32ab0b40732ff4c7d41f6e1322` | 5 run, 2 failures | **1** |
| HEAD | `ddcf59ff005dd910265a1b3468697617d7623f13` | 5 run, all passed | **0** |

### Fixed behaviors

- **Duplicate lines accumulate:** parent returned `{'a': 5, 'b': 4}` instead of expected `{'a': 3, 'b': 4}`. HEAD passes, including the input-preservation assertion.
- **Aggregate shortage is atomic:** parent failed with `AssertionError: ValueError not raised` for quantities 5 + 4 against stock 8. HEAD raises the expected `"insufficient stock"` error and preserves input stock. The parent’s failure prevented its subsequent input-preservation assertion from running.

### Passing controls on both

Distinct SKU deductions, empty orders returning a separate equal mapping, and rejection of zero/negative quantities and unknown SKUs.

### Confirmed native imports

Each process printed and asserted its copied module path:

```text
<WORKSPACE>/.allocation-compare-ud6rjr9_/before/allocation.py
<WORKSPACE>/.allocation-compare-ud6rjr9_/after/allocation.py
```

The existing helper captured the evidence and confirmed original file contents/modes unchanged and scratch copies removed. Git status remained clean; no report or harness was added.
