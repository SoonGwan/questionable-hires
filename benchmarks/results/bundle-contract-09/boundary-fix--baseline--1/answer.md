I’ll inspect eligibility within this project, run the 17/18/19 assertions before changing it, then make a focused fix and rerun the same tests.

Before the fix, ages 17 and 19 passed, and the new exactly-18 assertion failed as expected. I’ll change the comparison to include 18 and rerun the assertions unchanged.

Fixed eligibility to accept ages `>= 18` and retained the exactly-18 regression test.

Verification with `python3 -B -m unittest -v`:
- Before: 17 and 19 passed; 18 failed as intended.
- After: all three unchanged assertions passed.

Only the eligibility comparison and regression test changed.
