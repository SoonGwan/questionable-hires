I’ll read the Con Artist instructions, capture the project’s preservation state, and run the helper exactly once with the specified interpreter and unchanged recipe. I’ll report only evidence returned or directly verified.



The single Con Artist invocation completed with exit 0 (`observed`), using the specified interpreter and unchanged recipe.

| Mutation | Original test: correct / mutant | Stronger probe: correct / mutant | Actual assertion failure |
|---|---|---|---|
| Return 2 | Positive: pass / pass | Pass / fail | `assertEqual(value(), 1)`: `2 != 1` |
| Return 3 | Integer: pass / pass | Pass / fail | `assertEqual(value() * 2, 2)`: `6 != 2` |
| Return 4 | Positive: reused pass / pass | Pass / fail | `assertEqual(str(value()), "1")`: `'4' != '1'` |

All passes had native exit 0; probe failures had native exit 1. Each execution ran one test, with no skips, timeouts or truncated output.

**11 native executions:** two original baselines, three original mutant checks, three correct probes and three mutant probes. The third audit’s `#/audits/0/checks/correct_tests` references the first positive baseline; it adds no execution.

Every executed check reported project-local copied imports for `service` and `test_service`, with matching correct-source or distinct mutant hashes, and completed the same-process binding precheck. All six probes printed `Strong test binding verified` after asserting `value is service.value`.

No requested checks remain unrun. The original tests missed all three faults; the supplied stronger assertions detected their respective faults.

Helper integrity checks verified original bytes/modes, whole-project preservation including Git metadata, and owned-copy cleanup. An independent before/after inventory also matched. No report or harness was left behind.
