I’m using the con-artist skill to trace the dispatch assertions, run the native checks in disposable project-local copies, and verify any coverage gap with focused regression assertions.

The two existing tests cover ordered return values and deep payload isolation, but neither exercises a handler raising `ValueError`. I’ll check whether they pass with the swallowed-error fault, then verify assertions for the exception’s type/message and for stopping before later handlers run. The existing success tests will also run alongside those added checks.

**The original tests miss `swallowed-error`.** Both pass after the exact requested replacement in `dispatch.py`.

The implementation deep-copies each payload, collects results in registration order, and rethrows `ValueError` with its message. Existing tests assert ordered results, nested payload isolation, and unchanged caller state; neither exercises an error.

Executed in disposable project-local variants:

```sh
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v audit_binding
```

The temporary loader selected unchanged original tests, then those tests plus two identical regression tests.

| Checks | Implementation | Passed | Failed | Exit |
|---|---|---:|---:|---:|
| Original | Correct | 2 | 0 | 0 |
| Original | Swallowed error | 2 | 0 | 0 |
| Expanded | Correct | 4 | 0 | 0 |
| Expanded | Swallowed error | 2 | 2 | 1 |

Verified detecting assertions:

- `assertRaises(ValueError)` fails with **“ValueError not raised.”** Correct code also passes exact exception-type and message assertions.
- The event-list assertion expects only `first`, `fail`; faulty code additionally executes `later`.

Existing successful-dispatch controls pass in both expanded runs. Four native executions, 12 test executions; no baseline reuse. Failures were assertion failures, not setup or collection errors.

Every native process verified the variant’s module path, function code path, source hash, and test bindings.

Full project file/mode inventory remained unchanged, including Git metadata and supplied resources. Owned scratch was removed; no fixes, tests, harness, or report were retained.
