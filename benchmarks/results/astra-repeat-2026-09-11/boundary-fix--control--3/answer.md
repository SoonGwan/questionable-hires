I’ll check the eligibility rule and relevant tests, fix the age boundary, and run focused verification.

Fixed eligibility to accept customers aged 18 by changing `age > 18` to `age >= 18`.

Added a regression test that failed before the fix. All three tests now pass, covering ages 17, 18, and 19. `git diff --check` also passes. Only eligibility and its test file changed.
