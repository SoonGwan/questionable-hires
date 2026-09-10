I’ll check the eligibility rule, fix the age boundary, and run focused tests.

Changed eligibility to `age >= 18` and added a regression test for exactly 18.

Verified the new test failed before the fix. All 3 tests now pass, covering ages 17, 18, and 19. Only the eligibility rule and its test changed.
