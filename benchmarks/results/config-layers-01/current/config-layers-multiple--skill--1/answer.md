I’ll read the con-artist skill, then run the unchanged suite against correct code and each isolated fault in disposable project-local copies. I’ll verify imports inside each test process and remove all scratch files afterward.


The four existing tests cover each layer separately and a `None` override. They don’t check competing environment and override values, false-like values, or input mutation. I’ll test those gaps with the requested faults and log assertion values and copy-local bindings inside every unittest process.


The original suite detects **1 of 4 faults**; three survive.

Used the supplied Python with `-B -m unittest -v test_settings`. Every actual test process verified copy-local `settings.py`, `test_settings.py`, `test_settings.resolve is settings.resolve`, and the resolver’s code path.

| Original unchanged suite | Tests | Failures | Exit | Result |
|---|---:|---:|---:|---|
| Correct code | 4 | 0 | 0 | Pass |
| Reversed layer order | 4 | 0 | 0 | Survives |
| `if value:` | 4 | 0 | 0 | Survives |
| `result = defaults` | 4 | 0 | 0 | Survives |
| `if True:` | 4 | 1 | 1 | Detected: `test_absent_override` gets `{'retries': None}`, expects `{'retries': 3}` |

For each survivor, I appended one focused native assertion in disposable copies, preserving every existing assertion:

| Added check | Correct code | Faulty code | Actual assertion evidence |
|---|---|---|---|
| Competing layers: retries `3 → 4 → 5` | 5 tests, exit 0 | 5 tests, 1 failure, exit 1 | Correct `{'retries': 5}`; fault `{'retries': 4}` |
| Explicit `False`, `0`, `''` in both layers | 5 tests, exit 0 | 5 tests, 1 failure, exit 1 | Expected false-like values in both groups; fault retained `(True, 8, 'environment')` and `(True, 7, 'fallback')` |
| All three input mappings unchanged | 5 tests, exit 0 | 5 tests, 1 failure, exit 1 | Expected retries `(3, 4, 5)` across mappings; fault produced `(5, 4, 5)` |

All failures were assertion failures, with no import, setup, or empty-suite failures. **11 native executions, 50 tests total; no observations reused.**

Full-project file hashes and modes matched afterward, including source, tests, Git HEAD/index, and skill resources. All owned scratch was removed; no harness or report remains.
