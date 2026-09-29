I’ll use the con-artist skill to check the original tests against the exact isolated edit, then verify focused regressions for the no-predicate-call contract. I’ll confirm bindings inside each test process and remove all audit scratch afterward.


The selected tests check `maxsplit=0` output values with pure predicates, so they cannot observe the added calls. I’ll test a local call recorder and a raising predicate, plus generator output checks. The unchanged suite already supplies ordinary-split controls.


The exact `split_at` mutation **survived the original suite**. Identical focused regressions detected the consumer-contract violation.

All four executions used `<TEMP> -B -m unittest -v` in isolated copies:

| Code | Native selection | Tests | Exit | Result |
|---|---|---:|---:|---|
| Correct | Three requested class selectors | 13 | 0 | Passed |
| Faulty | Same unchanged selectors | 13 | 0 | Survived |
| Correct | Focused regressions | 3 | 0 | Passed |
| Faulty | Identical focused regressions | 3 | 1 | Four subtest failures |

The original assertions check output using pure predicates. The focused regressions expose:
- `assertEqual(calls, [])` receiving `[1, 0, 2]`, despite correct output.
- A deterministic raising predicate being invoked unexpectedly.

Both failures occur with default `keep_separator=False` and with `True`. Generator inputs, empty-input results, ordinary splits, and neighboring `split_before`/`split_after` checks passed.

Each native process verified copied package, implementation, test paths, public-function identities, and test bindings. Four executions total; original ordinary-split observations were reused as evidence, not rerun separately.

This establishes the explicit `maxsplit=0` consumer contract gap, not an upstream guarantee about callback counts in other modes.

Whole-project bytes/modes, including source, tests, license and Git metadata, remained unchanged. Installed resources were not modified. All owned scratch was removed; no report, harness, or fix remains.
