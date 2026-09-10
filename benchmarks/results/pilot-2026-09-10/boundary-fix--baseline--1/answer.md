I’ll find the eligibility check, fix the age boundary, and run focused tests.

Changed eligibility to `age >= 18` and added a regression test for exactly 18.

Verified the new test failed before the fix. All 3 tests now pass with `python3 -m unittest -v`, covering ages 17, 18, and 19. Only the eligibility condition and regression test changed.
