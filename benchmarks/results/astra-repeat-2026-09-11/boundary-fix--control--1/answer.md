I’ll check the eligibility rule and relevant tests, make a focused fix, and verify the age boundary.


Changed eligibility from `age > 18` to `age >= 18`.

Added a regression test for age 18 and confirmed it failed before the fix. All 3 tests now pass: 17 rejected, 18 and 19 accepted. `git diff --check` also passes.
