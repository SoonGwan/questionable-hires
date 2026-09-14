I’ll use the receipt skill to reproduce the age-18 failure, make a focused fix, and rerun the same assertions for ages 17, 18, and 19. I’ll keep all work within this project and preserve existing changes.

The before run reproduced the bug: ages 17 and 19 passed, while the exactly-18 assertion failed. I’ll change the eligibility comparison to include 18, then rerun these tests unchanged.

Fixed eligibility to accept `age >= 18` and retained the exactly-18 regression test.

Verification with `python3 -B -m unittest -v`:
- Before: 17 and 19 passed; 18 failed as expected.
- After: all three unchanged assertions passed.

`git diff --check` passed; reviewed changes touch only implementation and test. Existing `.agents/` files were preserved. Base revision: `dfd9adc`.
