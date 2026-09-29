I’ll read the Con Artist instructions and recipe, record the project’s preservation state, then invoke the helper exactly once with the specified interpreter. I’ll report only evidence available from that run.



The existing tests missed all three mutations; each stronger assertion passed on correct code and failed on its mutant.

Invoked exactly once, exiting 0 with `status: observed`:

```sh
<TEMP> -B .agents/skills/con-artist/scripts/audit.py --source . --spec recipe.json
```

| Mutation | Existing test | Correct / mutant native exit | Stronger correct / mutant exit | Actual assertion failure |
|---|---|---|---|---|
| `return 2` | `test_positive` | 0 / 0 | 0 / 1 | `assertEqual(value(), 1)`: `2 != 1` |
| `return 3` | `test_integer` | 0 / 0 | 0 / 1 | `assertEqual(value() * 2, 2)`: `6 != 2` |
| `return 4` | `test_positive` | 0 (reused) / 0 | 0 / 1 | `assertEqual(str(value()), "1")`: `'4' != '1'` |

There were **11 native executions**, each running one test: two original baselines, three mutant tests, three distinct correct probes and three mutant probes. The third original baseline references `#/audits/0/checks/correct_tests`; it was counted once. All commands used `python -B -m unittest`.

Every executed check reported project-local copied imports for `service` and `test_service`, with source hashes, and completed the same-process binding precheck. All six probe runs printed `Strong test binding verified` after asserting `value is service.value`; mutant tracebacks identified copied `test_stronger.py:9`.

No requested checks remain unrun; no timeouts, skips or truncated outputs occurred. Every audit verified original bytes/modes, whole-project protection including Git metadata, and owned-copy cleanup. Independent before/after inventories and Git status also matched. Recipe, production and tests remain unchanged; no report or harness was left.
