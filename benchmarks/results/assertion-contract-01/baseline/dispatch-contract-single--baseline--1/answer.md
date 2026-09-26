I’ll inspect dispatch and its tests, run the native checks in disposable correct and faulty copies, and verify focused regression assertions for any coverage gap. I’ll also confirm which dispatch file each test process loads and remove all scratch files.


The two existing tests cover result order, nested payload isolation, and unchanged caller state. Neither exercises a handler that raises `ValueError`, so the supplied fault appears uncovered. I’ll test exception type/message and whether later handlers run, alongside a successful dispatch that checks execution order and payload isolation.


The original tests **miss `swallowed-error`**. The implementation deep-copies each payload and rethrows `ValueError`; the fault instead appends `None` and continues.

| Checks | Correct | Swallowed-error |
|---|---|---|
| Original native tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Identical focused regressions | 2 passed; exit 0 | 2 tests, 3 assertion failures; exit 1 |

Original assertions cover ordered results, nested payload isolation, and unchanged caller state. They never exercise an exception. Execution order also lacks a direct assertion.

The added error regression detected:
- Missing `ValueError`: captured exception remained `None`.
- Missing message: expected `"handler rejected payload"`.
- Continued execution: calls were `["first", "fail", "later"]`, expected `["first", "fail"]`.

Caller-state assertions passed. The adjacent successful-dispatch regression passed on both variants, checking execution order, ordered results, independent nested payloads, and unchanged caller state.

Commands executed from each disposable variant directory:

```sh
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v variant_probe test_dispatch
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v variant_probe test_regression
```

`variant_probe` verified the dispatch module path, function code path, source SHA-256, and both test modules’ dispatch bindings inside every native process. No setup or collection failures occurred. Each correct suite ran once; no duplicate baseline run was needed.

All scratch files were removed. Source/tests and Git HEAD/index/status were verified unchanged. No report or harness remains.
