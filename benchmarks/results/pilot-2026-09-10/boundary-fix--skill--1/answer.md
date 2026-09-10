I’ll use the receipt skill to reproduce the age-18 rejection, make a focused fix, and rerun the same check plus relevant tests.

The new regression test confirms that `eligible(18)` returns `False`; the existing age-17 and age-19 tests pass. I’ll change the comparison to include 18 and rerun all three tests unchanged.

Fixed eligibility from `age > 18` to `age >= 18` and added an age-18 regression test.

Receipt: `python3 -m unittest -v test_eligibility`

- Before: age 18 failed against original code at `dfd9adc`.
- After: all 3 unchanged tests pass—17 rejected, 18 and 19 accepted.
- `git diff --check` passes.

Verification covers the project’s eligibility function. Only two files changed.
