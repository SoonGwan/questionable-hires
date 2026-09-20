I’m using the receipt skill to compare the parent and HEAD allocation modules with the same current tests and Python runtime, without changing project files.


The commit changes one line: repeated SKU quantities now accumulate. The existing comparison helper runs all five unchanged tests in isolated copies and reports the loaded module paths and process exits. I’ll use it and check file contents and modes, including Git metadata, before and after.


Verified: the one-line fix accumulates duplicate SKU quantities instead of overwriting them.

Ran `python3 -B tools/compare_allocation.py HEAD^ HEAD` using Python **3.9.6**, executable `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`. Both native unittest processes ran the same current five-test suite; only `allocation.py` varied.

| Test | Parent | HEAD |
|---|---|---|
| Duplicate lines accumulate | Failed: actual `{'a': 5, 'b': 4}`, expected `{'a': 3, 'b': 4}` | Passed |
| Aggregate shortage is atomic | Failed: `ValueError not raised` | Passed |
| Distinct lines control | Passed | Passed |
| Empty order control | Passed | Passed |
| Invalid order control | Passed | Passed |

**Revision and native process evidence**

- Parent: `481a3ccb54d84d32ab0b40732ff4c7d41f6e1322` — 5 tests, 2 failures, exit **1**.
- HEAD: `ddcf59ff005dd910265a1b3468697617d7623f13` — 5 tests passed, exit **0**.
- Each process verified and printed its copied import: project-relative `.allocation-compare-1xuz0hzn/before/allocation.py` and `.allocation-compare-1xuz0hzn/after/allocation.py`, respectively.

The fix corrects duplicate deductions and rejects combined quantities exceeding stock. HEAD also passes the associated input-preservation assertions; the parent failures prevented reaching those assertions. All three controls remain passing.

Comparison helper and final Git checks exited **0**. Project contents and modes, including `.git` and installed skill resources, were unchanged. Scratch copies were removed; no report or harness was retained.
