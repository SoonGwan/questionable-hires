I’ll inspect the eligibility check, run assertions for ages 17, 18, and 19 before editing it, then make a focused fix and rerun the same assertions.

The pre-fix run passed for ages 17 and 19 and failed at exactly 18, as expected. I’ll change the comparison to include 18 and keep the regression test.

Fixed eligibility to accept `age >= 18` and retained the exactly-18 regression test.

Verification: before the fix, assertions for 17 and 19 passed while 18 failed. After the fix, the same unchanged assertions all passed. Only the eligibility comparison and regression test changed.
