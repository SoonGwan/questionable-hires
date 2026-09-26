I’m using the con-artist skill to check the exact mutation against the selected native tests, then verify focused regressions if the mutation survives. I’ll confirm bindings inside each test process and remove all audit scratch afterward.


The selected tests cover `maxsplit=0` output values, but their predicates have no observable effects. The mutation should therefore preserve those assertions. I’ll add temporary regressions using a local call log and a raising predicate, covering generator input and both `keep_separator` settings, plus ordinary-split controls.


The exact `split_at` mutation **survives the original suite**. Identical additional regressions detect the consumer-contract violation.

| Native execution | Tests | Result | Exit |
|---|---:|---|---:|
| Original selectors, correct | 13 | Pass | 0 |
| Original selectors, faulty | 13 | Pass | 0 |
| Additional regressions, correct | 3 | Pass | 0 |
| Additional regressions, faulty | 3 | Four subtest failures | 1 |

All four processes used `<TEMP> -B -m unittest -v`. Original runs used your exact three class selectors, with assertions unchanged.

The detecting assertion was `self.assertEqual(calls, [])`: faulty code recorded `[1, 0, 2]`, although output remained `[[1, 0, 2]]`. A separate valid predicate raised a deterministic local `RuntimeError`, triggering an explicit test failure. Both witnesses detected the fault with `keep_separator=False` and `True`.

Empty-input checks, neighboring split functions, and ordinary `maxsplit=1` generator controls passed. Existing ordinary-split observations were reused as supporting evidence, without extra executions.

Each native process verified copied package, implementation and test paths, version `10.8.0`, public-function bindings, implementation code paths, and test globals.

This establishes the specified consumer contract gap; it makes no broader upstream callback-count promise or origin claim.

Whole-project integrity checks confirmed unchanged bytes/modes, including source, tests, license and Git metadata. Installed resources were untouched. All owned scratch was removed; no report, harness, fix or permanent changes remain.
