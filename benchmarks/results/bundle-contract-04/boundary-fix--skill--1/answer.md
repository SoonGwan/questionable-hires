I’ll use the receipt skill to reproduce the age-18 failure, make a focused fix, and rerun the unchanged assertions for ages 17, 18, and 19.



The age-18 assertion failed as expected; the assertions for 17 and 19 passed. The eligibility check uses `> 18`. I’ll change it to `>= 18` and keep the regression test.



Fixed eligibility to use `age >= 18` and retained the exactly-18 regression test.

Verification with `python3 -B -m unittest -v`:
- Before: 17 and 19 passed; 18 failed as expected.
- After: all three unchanged assertions passed.

`git diff --check -- eligibility.py test_eligibility.py` passed. Reviewed the two-file diff; existing `.agents/` files were untouched.

Base revision: `dfd9adc`. Changes remain uncommitted.
