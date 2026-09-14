I’ll inspect eligibility in this project, run assertions for ages 17, 18, and 19 before editing, then make the focused fix and rerun the same tests.

The pre-fix run passed for ages 17 and 19 and failed for exactly 18, as expected. I’ll change the threshold to include 18 and rerun the unchanged assertions.

Fixed eligibility to accept `age >= 18` and retained the exactly-18 regression test.

Verification with `python3 -B -m unittest -v`:
- Before: 17 and 19 passed; 18 failed as expected.
- After: all three unchanged assertions passed.

Only the eligibility comparison and regression test changed.
