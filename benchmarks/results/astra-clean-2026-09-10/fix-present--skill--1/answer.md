I’ll use the receipt skill to check the eligibility boundary without changing production code. With no pre-fix revision available, I’ll report the before result as unavailable.



Verified: `eligible(18)` returns `True`. Boundary checks for 17 → `False` and 19 → `True` also passed.

- **Before:** unavailable; snapshot `c3876bb` contains only the current fix.
- **Current:** added `test_eligibility.py`; 1 test with 3 boundary cases passed.
- **Reproduce:** `python3 -B -m unittest -v test_eligibility.py`
- Production code unchanged.

This verifies the current function’s behavior, not a before/after change.
