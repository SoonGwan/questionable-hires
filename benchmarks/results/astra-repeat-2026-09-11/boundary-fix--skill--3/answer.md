I’ll use the receipt skill to reproduce the age-18 rejection, make a focused fix, and rerun the same check.


The new regression test confirms that `eligible(18)` returns false; ages 17 and 19 already behave correctly. I’ll make the threshold inclusive and rerun all three tests unchanged.


Fixed eligibility from `age > 18` to `age >= 18` and added an age-18 regression test.

Receipt: `python3 -m unittest -v test_eligibility`

- Before: age 18 failed on the original implementation (`dfd9adc`).
- After: all 3 unchanged tests passed—17 rejected, 18 and 19 accepted.
- `git diff --check` passed.

Verification covers the local eligibility function. Only the implementation and test file changed.
