I’ll use the receipt skill to reproduce the age-18 rejection, make a focused fix, and rerun the same check.


The new regression test confirms that `eligible(18)` returns `False`; the existing age-17 and age-19 tests pass. I’ll change the cutoff to include 18.


Fixed eligibility to use `age >= 18` and added an age-18 regression test.

Receipt: `python3 -m unittest -v test_eligibility`

- Before: age 18 failed on the original implementation (`dfd9adc`).
- After: all 3 tests pass—17 rejected, 18 and 19 accepted.
- Same inputs and assertions before and after; `git diff --check` passed.

Verification covers the synthetic project’s eligibility function.
