I’ll inspect the eligibility code, run assertions for ages 17, 18, and 19 before changing it, then make a focused fix and rerun the same assertions.

The pre-fix run passed for ages 17 and 19 and failed for exactly 18, as expected. I’ll change the cutoff to include 18 and keep the regression test.

Fixed eligibility to accept ages `>= 18` and retained the exactly-18 regression test.

Verified with unchanged assertions for 17, 18, and 19:
- Before fix: 17 and 19 passed; 18 failed as expected.
- After fix: all three passed.

Only the eligibility comparison and regression test changed.
