I’m using the Con Artist skill to review the single helper run, separating returned evidence from unavailable observations and checking preservation and cleanup.


The single helper invocation returned `observed`, exit **0**, using unchanged `recipe.json` and the specified interpreter.

| Code | Native unittest outcome | Exact-value probe |
|---|---|---|
| Original | 1 test passed; exit 0 | Passed; exit 0 |
| Return 2 | 1 test passed; exit 0 | Exit 1: `AssertionError: 2` |
| Return 3 | 1 test passed; exit 0 | Exit 1: `AssertionError: 3` |
| Return 4 | 1 test passed; exit 0 | Exit 1: `AssertionError: 4` |

The existing positive-value assertion missed all three faults. The executed `value() == 1` probes detected each.

Both correct baselines executed **once**. Mutations 3 and 4 reused `#/audits/0/checks/correct_tests` and `#/audits/0/checks/correct_probe`: **8 executions total**, no requested mutation unrun.

Every executed check reported copied `service.py` import provenance, with SHA-256 prefixes `5d080563b572` (original), `d3fe37235936` (2), `865086861917` (3), and `953ceaf7ec00` (4). Function/code-object identity was not reported. No output was truncated and no check timed out.

All three audits verified selected original bytes/modes, whole-project preservation including in-root Git metadata, and owned-copy removal. No preservation failure occurred. No repair, restoration, additional report, or harness was created.
