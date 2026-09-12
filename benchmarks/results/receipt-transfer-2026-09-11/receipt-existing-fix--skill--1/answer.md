I’ll use the receipt skill to check the committed fix and compare the same boundary assertion before and after it in isolated copies, without changing existing project files.

Verified: commit `4fc5639` changes `> 5000` to `>= 5000`, accepting exactly 5000 cents.

Ran the unchanged regression test in isolated copies using `python3 -B -m unittest -v test_totals`:

- Before (`d2a7cf3`): exit **1**, failing specifically at 5000 (`False != True`).
- After (`4fc5639`): exit **0**. All boundaries pass: 4999 rejected, 5000 and 5001 accepted.

Evidence covers the repository’s `accepts_total` function. Existing project files were unchanged; temporary copies were removed.
