I’ll check the eligibility rule, fix the age boundary, and run the relevant tests.

Changed eligibility from `age > 18` to `age >= 18` and added a regression test for exactly 18.

All 3 tests pass: 17 rejected, 18 and 19 accepted. Only the eligibility rule and its test file changed.
