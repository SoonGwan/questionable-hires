I’ll use the installed Receipt skill, inspect the recipe and CLI, then run the comparison once and review its evidence without changing or restoring project files.


Ran the installed CLI exactly once with unchanged `recipe.json` and `<TEMP> CLI exit: **0**.

| Observation | Before `c3d6e180` | After `d8862faf` |
|---|---|---|
| Native/check exit | 1 / 1 | 0 / 0 |
| Tests | 3, boundary failed | 3, all passed |
| Actual/expected: above | true/true | true/true |
| Actual/expected: below | false/false | false/false |
| Actual/expected: boundary | false/true | true/true |

Both runs verified importing `rule` from their respective `.receipt-v88c0g9u/{before,after}/rule.py` copies, with PIDs 20361 and 20362. Assertion observations were complete within the declared current-thread scope; neither run skipped tests, timed out, or truncated output.

**Preservation established within the guard’s scope:** 62 project entries, including Git metadata, were unchanged. Selected original bytes/modes, including `notes.txt`, were unchanged. Owned comparison copies were reported removed.

No requested evidence was missing. The guard excludes symlink targets and timestamps; import provenance establishes import-time location. No repair, restoration, or additional report was made.
