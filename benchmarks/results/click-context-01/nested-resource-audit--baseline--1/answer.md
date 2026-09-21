I’ll inspect the context tests and unwinding path, then run the relevant unchanged tests and any needed focused assertions against isolated correct and mutated copies. I’ll remove all temporary files and check that the originals remain unchanged.

The final nested non-suppression case registers both resources outside `ctx.scope()`. Its `pytest.raises` catches the explicit raise without unwinding either resource. The single-resource propagation and nested suppression cases do enter a scope. I’ll verify these paths in the native pytest process and test a mutation that incorrectly suppresses an exception after multiple resources decline it.

Coverage is missing. The correct implementation propagates the original exception and exits both resources in reverse registration order, but the existing nested non-suppression case does not exercise that behavior.

In `tests/test_context.py::test_with_resource_nested_exception`, the final `pytest.raises(TestException)` block at line 655 omits `with ctx.scope():`. Native tracing confirmed **two resource entries, zero exits, and two callbacks still pending**. The explicit raise satisfies `pytest.raises` directly.

The neighboring controls do exercise unwinding:

- `tests/test_context.py::test_with_resource`: asserts the resource changes from `[1]` to `[0]` after cleanup.
- `tests/test_context.py::test_with_resource_exception`: its non-suppressing case enters a scope. Tracing confirmed one resource exit returning `False`, followed by propagation into `pytest.raises`. It does not assert exception identity or resource state afterward.
- `tests/test_context.py::test_with_resource_nested_exception`: the suppression cases exit inner then outer. Inner suppression produces assertions `rv_nested == [12]`, `rv == [0]`; inner refusal followed by outer suppression produces `[12]`, `[2]`.

I mutated only the disposable faulty copy’s actual `src/click/core.py`: `_close_with_exception_info` incorrectly returns `True` after unwinding when an exception exists, multiple callbacks were registered, and `ExitStack` returned false.

| Native pytest selection | Correct copy | Faulty copy |
|---|---:|---:|
| Three unchanged existing tests above | 3 passed; exit 0 | 3 passed; exit 0 |
| `tests/test_context_audit.py::test_two_resources_decline_body_exception` | 1 passed; exit 0 | 1 failed; exit 1 |

The temporary added test registers outer then inner inside `ctx.scope()`, with both exits returning `False`. Its six assertions check registration order, exact exit order `["inner", "outer"]`, exception type, original exception identity received by both resources, non-null tracebacks, and propagated exception identity.

Both variants passed the cleanup assertions. The faulty variant failed specifically at `assert caught is original`: `caught` was `None`. This was behavioral mutation detection, not a setup failure.

The exercised path was `scope()` → `Context.__exit__()` → `_close_with_exception_info()` → `ExitStack.__exit__()`. Every native pytest process verified copy-local `click.__file__`, `click.core.__file__`, and the executed method’s source filename.

All runs used the supplied interpreter with bytecode disabled, the required environment and cache settings, and unchanged project pytest settings. Disposable files were removed in `finally`. Repository-wide content hashes and modes matched afterward, including Git HEAD/index; no harness, report, or production changes remain.
