I’ll use the receipt skill to reproduce the age-18 rejection, make a focused fix, and rerun the same check.


The new regression test confirms that `eligible(18)` returns `False`; ages 17 and 19 already behave correctly. I’ll change the comparison to include 18 and rerun all three tests unchanged.


Fixed eligibility from `age > 18` to `age >= 18` and added an age-18 regression test.

Receipt using the same command before and after:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_eligibility
```

- **Before:** Age 18 failed on the original implementation at `dfd9adc`.
- **After:** All 3 tests passed, covering ages 17, 18, and 19. Assertions unchanged.
- `git diff --check` passed.

Verification covers the synthetic project’s eligibility function. Only implementation and regression test changed.
