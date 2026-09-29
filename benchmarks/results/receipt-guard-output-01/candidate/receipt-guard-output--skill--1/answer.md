I’ll read the Receipt instructions, run the comparison exactly once, and review the returned evidence and cleanup without changing or restoring project files.

I’m using the Receipt skill. The unchanged recipe requests assertion observations, copied-import verification, a watch on `notes.txt`, and a tree preservation check. I’ll run it once and keep any unavailable evidence explicitly marked as unavailable.

Ran the installed Receipt CLI exactly once with `<TEMP> and unchanged `recipe.json`.

- **Before** (`f1f14030baded339863f92bbe9d4520c10315ada`): native/check exit **1**; 3 tests, none skipped. Boundary failed: actual `False`, expected `True`.
- **After** (`e2835b5b02365357d4a2eec80505f73a65db651e`): native/check exit **0**; all 3 tests passed. Boundary observed `True`, expected `True`.
- Both recorded above/below assertion pairs as `True/True` and `False/False`. Assertion observations were complete within their declared scope; neither output was truncated or timed out.
- Native processes verified importing `rule` from `.receipt-f_ecyv_3/before/rule.py` (PID 21829) and `.receipt-f_ecyv_3/after/rule.py` (PID 21830).

**Preservation was not established.** CLI exit **2**, status `incomplete`: selected-original protection reported only `notes.txt` changed, with no restoration. Whole-tree/Git preservation remains **unverified** (`tree_guard.unchanged: null`). Passing native tests do not override that failure.

Owned comparison copies were reported removed. No repair, restoration, additional test run, report, or harness was created.
