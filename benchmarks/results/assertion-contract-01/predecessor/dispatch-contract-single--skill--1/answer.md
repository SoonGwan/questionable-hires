I’ll use the con-artist skill to inspect the dispatch tests, run the specified fault in disposable project-local copies, and verify any needed regression assertions. I’ll preserve the supplied files and Git state and remove all scratch files.

The two existing tests check result order, payload isolation, and unchanged caller state, but neither handler raises an error. I’ll test whether the specified fault survives them, then check focused assertions for error propagation and stopping later handlers, alongside successful dispatch. Each native test process will verify its dispatch binding points to the copied variant.

**The original tests miss `swallowed-error`.** Both pass after the exact replacement in `dispatch.py`.

The implementation deep-copies the payload for each handler, collects results sequentially, and rethrows `ValueError` with its message. Existing assertions check ordered results (`test_dispatch.py:7`), independent payload values (`:14`), and unchanged caller state (`:15`). Neither test exercises an exception.

Executed in disposable project-local copies using `/opt/homebrew/opt/python@3.11/bin/python3.11`:

| Checks | Correct implementation | Faulty implementation |
|---|---|---|
| Original tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Original + focused regressions | 5 passed; exit 0 | 3 passed, 2 failed; exit 1 |

Native commands:

```sh
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v test_dispatch
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v test_dispatch test_dispatch_regression
```

The same additional assertions ran against both implementations:

- `assertRaises(ValueError)` detected **“ValueError not raised.”** Correct code also passed exact exception-type and message assertions.
- An event-list assertion detected the forbidden `"later"` handler executing after failure.
- Successful-dispatch assertions verified execution order, ordered results, independent nested payloads, and unchanged caller state; these passed on both variants.

All four native processes verified copied module provenance, function code location, and test bindings. There were no setup/collection failures, skips, or timeouts. Four executions total; no baseline reuse.

The preservation inventory confirmed unchanged project files and Git metadata. All owned scratch was removed; no report, harness, or test edits were retained.
