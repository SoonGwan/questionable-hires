I’ll inspect the resolver and native tests, then run the unchanged suite against correct code and each isolated fault in disposable project-local copies. I’ll verify imports and the resolver binding inside each test process, add regressions for survivors, and remove the scratch files.


The original suite has four tests. It covers `None` in an override, but has no assertion for competing environment and override values, falsy values, or input mutation. I’ll run all four faults to confirm which survive and record the assertion values in each native test process.


The original suite detects **1 of 4 faults**; three survive.

| Original suite against | Tests | Failures | Exit | Outcome |
|---|---:|---:|---:|---|
| Correct code | 4 | 0 | 0 | Pass |
| Reversed layer order | 4 | 0 | 0 | Survives |
| `if value:` | 4 | 0 | 0 | Survives |
| `result = defaults` | 4 | 0 | 0 | Survives |
| `if True:` | 4 | 1 | 1 | Detected: `test_absent_override` gets `{'retries': None}`, expects `{'retries': 3}` |

For each survivor, I appended a focused native regression in disposable copies, preserving every existing assertion:

| Regression | Correct code | Isolated fault | Observed fault assertion |
|---|---|---|---|
| Competing layers: retries 3 → 4 → 5 | 5 tests, exit 0 | 5 tests, 1 failure, exit 1 | Actual `{'retries': 4}`; expected `{'retries': 5}` |
| Explicit falsy values | 5 tests, exit 0 | 5 tests, 1 failure, exit 1 | Actual `{'enabled': True, 'retries': 3, 'label': 'default'}`; expected `{'enabled': False, 'retries': 0, 'label': ''}` |
| All three inputs unchanged | 5 tests, exit 0 | 5 tests, 1 failure, exit 1 | Actual retries across inputs `(5, 4, 5)`; expected `(3, 4, 5)` |

The falsy regression passes for both environment and overrides on correct code. The fault fails its first, environment assertion; its override assertion is consequently not reached.

All **11 executions / 50 native tests** used the supplied Python 3.11.16 and `unittest`. Before every test, inside its actual process, checks verified copy-local module paths, resolver code location, and the test’s `resolve` binding identity. No import, setup, or empty-suite failures counted as detection.

The original correct baseline was executed once and **reused** for the four unchanged-suite comparisons. Each regression had a separate correct-code execution.

Cleanup succeeded. Original file bytes and modes, including Git HEAD/index, remained identical. Skill resources were untouched; no scratch, harness, or report remains.
