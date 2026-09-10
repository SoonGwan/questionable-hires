I’ll inspect the eligibility rule and relevant tests, fix the age boundary, and run focused checks.

Fixed eligibility from `age > 18` to `age >= 18`.

Added an age-18 regression test and confirmed it failed before the fix. All three tests now pass: 17 rejected, 18 and 19 accepted. `git diff --check` also passes. Only the rule and its test changed.
