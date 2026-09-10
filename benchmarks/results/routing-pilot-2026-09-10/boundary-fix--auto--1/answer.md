I’ll inspect the eligibility check, make a focused fix, and verify the age-18 boundary locally.


The check uses `age > 18`, which rejects 18-year-olds. I’ll use the project’s local receipt skill to verify a failing test before the fix and a passing test afterward.


Fixed eligibility to accept `age >= 18` and added an age-18 regression test.

Verified with `python3 -m unittest -v test_eligibility`:
- Before: age-18 test failed.
- After: all 3 tests passed, covering ages 17, 18, and 19.

Only the eligibility check and its test changed. Verification was local.
