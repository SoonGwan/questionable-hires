I’ll inspect the implementation and tests, run each fault separately in disposable project-local copies, and check any coverage gaps with focused assertions. I’ll verify which dispatch file each test process loads and remove all scratch files afterward.


The two existing tests cover ordered return values, payload isolation between handlers, and unchanged caller state. Neither exercises `ValueError`. I’ll test exception type/message and stopping later handlers separately, with a nearby success case that checks execution order, results, and payload isolation.


The original tests detect **2 of 3 faults**. They miss `swallowed-error`; focused regression assertions detect it.

Each variant used a separate project-local copy with exactly one replacement. Commands executed from each variant directory:

```sh
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v test_variant_origin test_dispatch
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v test_variant_origin test_regression
```

Counts below include one provenance test per process:

| Variant | Original: tests / failures / exit | Focused: tests / failures / exit |
|---|---:|---:|
| Correct | 3 / 0 / 0 | 4 / 0 / 0 |
| swallowed-error | 3 / 0 / 0 | 4 / 2 / 1 |
| reversed-handlers | 3 / 2 / 1 | 4 / 2 / 1 |
| shared-payload | 3 / 1 / 1 | 4 / 1 / 1 |

The unchanged correct results were **reused as the baseline** for all three fault comparisons.

- **swallowed-error:** Original tests contain no exception assertions. Added `assertRaises(ValueError)` fails with “ValueError not raised”; a separate call-log assertion observes `['fail', 'later']` instead of `['fail']`. Correct code passes exact exception type and message assertions. Nearby successful dispatch passes both implementations.
- **reversed-handlers:** Original `test_order` observes `['second', 'first']`; `test_payload_isolation` also fails because returned values appear in reverse order. Focused assertions independently detect reversed execution through handler call logs.
- **shared-payload:** Original `test_payload_isolation` observes both returned payloads containing `[1, 2]`, detecting shared mutation. Its subsequent caller-state assertion is not reached after that failure. The focused success test also detects shared mutation.

Implementation review confirms registration-order iteration, per-handler `deepcopy`, ordered result collection, and immediate propagation through `ValueError(str(error))`.

All eight native test processes verified the loaded module path, function code path, original test’s imported function identity, and variant source SHA-256. All reported failures were assertion failures; there were no setup or collection errors.

Scratch was removed in `finally`. Content snapshots confirmed supplied files and all Git files unchanged. No harness/report remains; no installs, network access, or production changes occurred.
