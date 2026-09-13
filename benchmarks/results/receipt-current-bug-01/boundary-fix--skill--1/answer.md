I’m using the receipt skill to reproduce the age-18 rejection, make a focused fix, and verify the same regression passes afterward.

Changed eligibility to `age >= 18` and added an age-18 regression test.

Verification with `python3 -m unittest -v`:
- Before: age-18 test failed; ages 17 and 19 passed.
- After: all three unchanged tests passed.

Focused diff reviewed; `git diff --check` passed.
