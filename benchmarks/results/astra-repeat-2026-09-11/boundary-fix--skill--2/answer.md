I’ll use the receipt skill to reproduce the age-18 rejection, make a focused fix, and rerun the same check.



Fixed eligibility from `age > 18` to `age >= 18` and added an age-18 regression test.

Receipt: `python3 -m unittest -v test_eligibility`

- Before: age 18 failed; ages 17 and 19 passed.
- After: all 3 tests passed with unchanged assertions.
- `git diff --check` passed.

Verification covers the real eligibility function in this synthetic project.
