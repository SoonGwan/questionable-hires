I’m using the receipt skill to capture the age-18 failure, make a focused fix, and rerun the same assertions for ages 17, 18, and 19.

The before run confirmed the defect: ages 17 and 19 passed, while exactly 18 failed. I’m changing the cutoff to include 18 and retaining the regression test.

Fixed eligibility to use `age >= 18` and retained the exactly-18 regression test.

Verification with `python3 -B -m unittest -v`:
- Before: 17 and 19 passed; 18 failed as intended.
- After: all three unchanged assertions passed.

`git diff --check` passed. Reviewed changes affect only eligibility and its test; existing `.agents/` files were preserved. Base revision: `dfd9adc`.
