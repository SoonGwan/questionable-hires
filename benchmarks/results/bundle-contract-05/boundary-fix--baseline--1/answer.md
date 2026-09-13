I’ll inspect the eligibility check, run assertions for ages 17, 18, and 19 before changing it, then apply a focused fix and rerun the same assertions.

The pre-fix run passed for ages 17 and 19 and failed for exactly 18, as expected. I’ll change the comparison to include 18 and keep the regression test.

Fixed eligibility to accept `age >= 18` and retained the exactly-18 regression test.

Verification with unchanged assertions:
- Before fix: ages 17 and 19 passed; age 18 failed as expected.
- After fix: all three passed.

Only the eligibility comparison and regression test changed.
