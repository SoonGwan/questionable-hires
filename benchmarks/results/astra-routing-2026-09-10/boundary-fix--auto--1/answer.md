I’ll inspect the eligibility check, make a focused fix, and verify that age 18 passes while younger customers remain rejected. I’m using the receipt skill to verify the behavior change.


The check uses `age > 18`, and the existing tests cover only ages 17 and 19. I’ll add a regression test for age 18 and change the comparison to include it. I’m also applying the hostage-negotiator skill to keep the scope limited.


Changed eligibility to `age >= 18` and added an age-18 regression test.

Verified with `python3 -B -m unittest -v test_eligibility`: the new test failed before the fix; all three tests pass afterward. Age 17 remains rejected, and ages 18 and 19 pass.

Only the eligibility comparison and regression test changed.
