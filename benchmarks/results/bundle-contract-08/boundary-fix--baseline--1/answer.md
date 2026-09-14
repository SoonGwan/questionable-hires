I’ll inspect the eligibility code, run assertions for ages 17, 18, and 19 before changing it, then make a focused fix and rerun the same tests.

The pre-fix run passed for ages 17 and 19 and failed for exactly 18 as expected. I’ll change the comparison to include 18 and retain the regression test.

Fixed eligibility to accept ages **18 and older**. Retained the exactly-18 regression test.

Verification with unchanged assertions:
- Before fix: ages 17 and 19 passed; age 18 failed as expected.
- After fix: all three passed.

Only the eligibility comparison and regression test changed.
