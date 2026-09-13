I’ll use the receipt skill to run the 17, 18, and 19 assertions before the fix, then rerun them unchanged and retain the regression test. I’ll keep all work inside this project.

The before run reproduced the bug: the age-18 assertion failed, while ages 17 and 19 passed. I’ll change the boundary to include 18 and rerun the same assertions.

Fixed eligibility to use `age >= 18` and retained the exactly-18 regression test.

Verification with `python3 -B -m unittest -v`:
- Before: 18 failed; 17 and 19 passed.
- After: all three unchanged assertions passed.

`git diff --check` passed. Reviewed changes affect only eligibility and its test, based on `dfd9adc`. Existing `.agents/` files were preserved.
