I’ll read the Con Artist instructions, check preservation, then run the helper exactly once and review its returned evidence.

The original tests missed all three faults; the stronger assertion detected each.

Ran exactly once with unchanged `recipe.json`:
```sh
<TEMP> -B .agents/skills/con-artist/scripts/audit.py --source . --spec recipe.json
```
Helper exit: **0**, status: `observed`.

| Mutation | Original selection | Correct / mutant native exit | Stronger correct / mutant exit | Actual failure |
|---|---|---|---|---|
| Return 2 | `test_positive` | 0 / 0 | 0 / 1 | `AssertionError: 2 != 1` |
| Return 3 | `test_integer` | 0 / 0 | 0 / 1 | `AssertionError: 3 != 1` |
| Return 4 | `test_positive` | 0 (reused) / 0 | 0 / 1 | `AssertionError: 4 != 1` |

All stronger failures occurred at copied `test_stronger.py:9`, `self.assertEqual(value(), 1)`.

**11 native executions**, each running one test through `python -B -m unittest`: two original baselines, three original mutant checks, three correct probes, three mutant probes. The third original baseline references `#/audits/0/checks/correct_tests`; it adds no execution. Correct probes actually ran separately.

Every executed check reported project-local copied imports of `service` and `test_service`, their hashes, and completed same-process binding prechecks. Every probe printed `Strong test binding verified` after confirming `value is service.value`; mutant tracebacks identified the copied probe files.

No requested checks remain unrun; no skips, timeouts, or truncated outputs occurred. All integrity checks verified original bytes/modes, whole-project preservation including Git metadata, and owned-copy cleanup. Git status and HEAD also matched before/after. No report, harness, or implementation changes were left.
