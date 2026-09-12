I’ll use the receipt skill to reproduce the age-18 rejection, make a focused fix, and rerun the same regression check.


The new regression test reproduces the bug: `eligible(18)` returns false, while the existing checks for 17 and 19 pass. I’ll change the comparison to include 18.


Fixed eligibility to use `age >= 18` and added an age-18 regression test.

Receipt: `python3 -m unittest -v test_eligibility`

- Before: age 18 failed on revision `dfd9adc`; exit 1.
- After: the unchanged test passed alongside ages 17 and 19; exit 0.

Verification covers the real eligibility function in this synthetic project; no external integration was tested.
