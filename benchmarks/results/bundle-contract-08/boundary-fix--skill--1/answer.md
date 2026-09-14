I’ll use the receipt skill to reproduce the age boundary failure, make a focused fix, and rerun the same assertions while retaining the regression test. All work will stay within this project.

The before run passed for ages 17 and 19 and failed exactly as intended for age 18. The eligibility check uses `> 18`; I’ll change it to `>= 18` and rerun the unchanged tests.

Fixed eligibility to accept `age >= 18` and retained the exactly-18 regression test.

Verification with unchanged assertions: `python3 -B -m unittest -v`
- Before: ages 17 and 19 passed; age 18 failed.
- After: all three passed.
- `git diff --check -- eligibility.py test_eligibility.py` passed.

Reviewed the two-file diff against base `dfd9adc`; existing `.agents/` files were untouched.
