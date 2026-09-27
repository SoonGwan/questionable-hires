I’ll use the Con Artist skill, inspect the recipe, and invoke the helper exactly once with the specified interpreter. I’ll report returned evidence and identify any observations the helper does not provide.

The single helper invocation exited **0** with `status: observed`. Existing tests missed all three faults; the stronger inline assertion detected each.

| Code | Native unittest result | Inline `value() == 1` probe |
|---|---|---|
| Original | 1 test, OK; exit 0 | Exit 0 |
| Return 2 | 1 test, OK; exit 0 | Exit 1: `AssertionError: 2` |
| Return 3 | 1 test, OK; exit 0 | Exit 1: `AssertionError: 3` |
| Return 4 | 1 test, OK; exit 0 | Exit 1: `AssertionError: 4` |

The original test and probe each executed once. Mutations 2 and 3 reused `#/audits/0/checks/correct_tests` and `#/audits/0/checks/correct_probe`: **eight executed checks total**, with no requested mutation unrun.

Every executed check reported the specified interpreter and copied `service.py` provenance. SHA-256 prefixes were `5d080563b572` (original), `d3fe37235936` (2), `865086861917` (3), and `953ceaf7ec00` (4), matching between corresponding test/probe copies. Separate test-module or function-identity evidence was not returned. No timeout or output truncation occurred.

All three integrity results verified selected original bytes/modes, whole-project preservation including in-root Git metadata, and owned-copy cleanup. No preservation failure occurred. No repairs, restoration, report, or harness were created.
