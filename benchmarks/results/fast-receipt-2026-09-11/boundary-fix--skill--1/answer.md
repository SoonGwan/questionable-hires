I’ll use the receipt skill to reproduce the age-18 rejection, make a focused fix, and rerun the same assertion.


Fixed eligibility from `age > 18` to `age >= 18` and added an age-18 regression test.

Receipt: `python3 -m unittest -v test_eligibility`

- Before: on `dfd9adc` plus the new test, age 18 failed (exit 1).
- After: unchanged tests all passed (exit 0): 17 rejected; 18 and 19 accepted.

Verification covers the project’s eligibility function directly. Only implementation and regression test changed.
