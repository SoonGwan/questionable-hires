I’ll read the installed Receipt instructions, run the comparison exactly once, and review the returned evidence and preservation checks without changing or restoring project files.


Ran the installed Receipt CLI exactly once with unchanged `recipe.json`. CLI exit: **0**, status: `observed`.

| Returned evidence | Before `c3d6e180…` | After `d8862faf…` |
|---|---|---|
| Native/helper exit | 1 / 1 | 0 / 0 |
| Tests | 3 run, 0 skipped; boundary failed | 3 run, 0 skipped; all passed |
| Actual/expected assertion values, in order | true/true, false/false, **false/true** | true/true, false/false, **true/true** |

Both processes verified importing `rule.py` from their respective `.receipt-nl2p2hac/{before,after}/` copies (PIDs 21101/21102). Assertion observations were complete within the declared scope; neither output was truncated or timed out.

**Preservation passed within the guard’s scope:** selected originals, including `notes.txt`, and the source tree including Git metadata were reported unchanged. No original-state change was reported. Owned comparison copies were removed.

No requested evidence was missing. Import provenance establishes import-time location; preservation checks do not cover timestamps, symlink targets, or transient changes. No repair, restoration, additional test execution, report, or harness was created.
