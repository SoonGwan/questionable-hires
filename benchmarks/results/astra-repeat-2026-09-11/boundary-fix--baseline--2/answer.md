I’ll inspect the eligibility check, fix the age boundary, and run focused verification.

Changed eligibility to `age >= 18` and added a regression test for exactly 18.

Verified the new test failed before the fix. All three tests—ages 17, 18, and 19—now pass with `python3 -m unittest -v`. Diff checks pass.
