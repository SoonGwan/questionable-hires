I’ll use the receipt skill to run the 17, 18, and 19 assertions before changing implementation, then rerun them unchanged after a focused fix and retain the regression test.

The before run reproduced the bug: ages 17 and 19 passed, while the exactly-18 assertion failed. I’ll change the comparison to include 18 and rerun the same tests unchanged.

Fixed eligibility to use `age >= 18` and retained the exactly-18 regression test.

Verification with `python3 -B -m unittest -v`:
- Before: 17 and 19 passed; 18 failed as expected.
- After: all three unchanged assertions passed.
- `git diff --check -- eligibility.py test_eligibility.py` passed.

Reviewed the two-file diff against base `dfd9adc`. Existing `.agents/` files were untouched.
