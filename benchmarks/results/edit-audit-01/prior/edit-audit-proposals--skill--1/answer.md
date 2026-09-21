I’ll use the con-artist skill to run both unchanged tests against correct code and each isolated fault, trace their runtime bindings, then remove the disposable copies.



`test_multiple_edits` checks only the result’s type and length, so it may miss misplaced characters and caller-list mutation. `test_overlap` checks the exception type and message, but never inspects the list afterward. I’ll trace each native test’s call to confirm the copied function binding and record its result or exception and any list mutation.



Only overlap-rejection removal was detected, and only by `test_overlap`. The other five fault/test combinations passed.

Ran these commands from each disposable variant root, with unchanged test files:

```sh
python3 -B -m unittest test_edits.EditTests.test_multiple_edits -v
python3 -B -m unittest test_edits.EditTests.test_overlap -v
```

Both correct-code tests passed (exit 0). These baselines apply to all three comparisons: multiple edits returned `"αQδεXYθ"`; overlap raised `ValueError("overlapping edits")`; neither changed its caller list.

Each fault was confined to `apply_edits`: forward application replaced `reversed(ordered)` with `ordered`; overlap removal deleted only the overlap check; in-place sorting replaced `sorted(...)` with `edits.sort(...)` and `ordered = edits`.

| Fault | Native test | Result and explanation |
|---|---|---|
| Forward application | `test_multiple_edits` | **Survived, exit 0.** Returned incorrect `"αQδεζXY"`. The assertions check only `str` and length 7, which still hold. |
| Forward application | `test_overlap` | **Survived, exit 0.** Overlap validation raises the expected exception before application; the faulty loop is unreachable. |
| No overlap rejection | `test_multiple_edits` | **Survived, exit 0.** Its ranges do not overlap, so it returns the correct result. |
| No overlap rejection | `test_overlap` | **Detected, exit 1.** Returned `"aXf"`; `assertRaisesRegex(ValueError, "overlapping edits")` failed with `AssertionError: ValueError not raised`. |
| In-place sorting | `test_multiple_edits` | **Survived, exit 0.** Correct result, but caller order changed to `[(1, 3, "Q"), (5, 7, "XY")]`. No assertion checks preservation. |
| In-place sorting | `test_overlap` | **Survived, exit 0.** Expected exception, but caller order changed to `[(1, 4, "X"), (3, 5, "Y")]` before raising. No assertion checks preservation on failure. |

Instrumentation in **each native test process** confirmed the copied implementation and test-module paths, `test_edits.apply_edits is text_edits.apply_edits`, and that the executing frame used that function’s code object. It also recorded implementation hashes, results, exceptions, and list changes. There were **no setup failures**; the single failure was behavioral detection.

Concrete proposed assertions, **not added or executed**:

- For forward application: `self.assertEqual(result, "αQδεXYθ")` on the existing valid multiple-edit input. The overlap test would need an additional valid-input case to reach application.
- For missing overlap rejection: add the existing overlapping-input `assertRaisesRegex` case wherever independent overlap coverage is desired; non-overlapping input cannot distinguish this fault.
- For caller preservation: save `before = edits.copy()` and assert `self.assertEqual(edits, before)` after success and after the expected exception. The overlap case must retain its list in a variable.

All disposable copies were removed. Whole-project before/after checks confirmed unchanged original file bytes and modes, including Git metadata; no harness or report remains.
