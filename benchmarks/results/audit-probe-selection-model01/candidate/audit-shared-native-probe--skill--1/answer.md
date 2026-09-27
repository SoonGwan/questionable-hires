I’ll read the Con Artist instructions, run the helper exactly once with the specified interpreter and unchanged recipe, then review its evidence and verify preservation and cleanup.



The existing tests missed all three faults; the stronger assertion detected each one.

Ran the installed helper exactly once with unchanged `recipe.json` and `<TEMP> CLI exit: **0**, status: `observed`.

| Mutant | Original selection | Correct code | Mutant | Stronger mutant assertion |
|---|---|---|---|---|
| Return 2 | `test_positive` | Pass, exit 0 | Pass, exit 0 | `2 != 1`, exit 1 |
| Return 3 | `test_integer` | Pass, exit 0 | Pass, exit 0 | `3 != 1`, exit 1 |
| Return 4 | `test_positive` | Reused pass | Pass, exit 0 | `4 != 1`, exit 1 |

The stronger test passed on correct code. Each mutant failed at `test_stronger.py:9`: `self.assertEqual(value(), 1)`.

**Nine native executions** ran via `python -B -m unittest`, each running one test: two original baselines, three mutant originals, one stronger baseline, three stronger mutants. Audit 3’s original baseline references `#/audits/0/checks/correct_tests`; audits 2 and 3’s stronger baselines reference `#/audits/0/checks/correct_probe`. These references add no executions.

Every executed check reported copied `service` and `test_service` imports and completed the same-process binding precheck. Service hashes distinguished correct and mutant code; the test hash stayed unchanged. All four stronger executions printed `Strong test binding verified` after confirming `value is service.value`; mutant tracebacks located the assertion inside their disposable copies.

No requested checks remain unrun; no timeouts, skips, or truncated outputs occurred. Every audit verified original bytes/modes, whole-project preservation including Git metadata, and owned-copy cleanup. No report, harness, or implementation changes were left.
