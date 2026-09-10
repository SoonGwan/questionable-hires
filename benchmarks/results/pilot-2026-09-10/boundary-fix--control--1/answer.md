I’ll inspect the eligibility check, fix the age boundary, and run the relevant tests.

Fixed eligibility from `age > 18` to `age >= 18`.

Added a regression test for exactly 18 and confirmed it failed before the fix. All 3 tests now pass, covering ages 17, 18, and 19. `git diff --check` also passes.

Only the eligibility condition and regression test changed.
