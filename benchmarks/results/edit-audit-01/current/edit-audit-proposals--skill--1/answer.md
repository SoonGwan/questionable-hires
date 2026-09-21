I’m using the con-artist skill to run the six fault/test combinations in disposable project-local copies, verify their runtime bindings, and leave the original files unchanged.

The multiple-edits test checks only the result’s type and length, so it may miss misplaced text and caller-list mutation. The overlap test checks the exception message. I’ll trace each native test run to confirm the copied function it calls and record its return value or exception, plus any change to the input list.

Completed all six combinations with unchanged native test bodies. **Only `test_overlap` detects omitted overlap rejection.** The other five combinations pass.

Each copy root ran:

```sh
python3 -B -m unittest test_edits.EditTests.test_multiple_edits -v
python3 -B -m unittest test_edits.EditTests.test_overlap -v
```

Both correct-code tests passed (exit 0); these baselines apply to all three independent variants.

| Fault confined to `apply_edits` | `test_multiple_edits` | `test_overlap` |
|---|---|---|
| Apply sorted edits forward using original offsets | **Survives, exit 0.** Returns incorrect `'αQδεζXY'`; type and length assertions still pass. Correct result: `'αQδεXYθ'`. | **Survives, exit 0.** Overlap validation raises before application reaches the fault. |
| Remove overlap rejection, retain range validation | **Survives, exit 0.** Its nonoverlapping input still returns the correct result. | **Detected, exit 1.** Returns `'aXf'`; `assertRaisesRegex(ValueError, "overlapping edits")` fails with `ValueError not raised`. |
| Sort caller list in place; preserve other behavior | **Survives, exit 0.** Correct result, but caller list is reordered. Neither assertion checks it. | **Survives, exit 0.** Expected exception occurs, but caller list is reordered before raising. No preservation assertion exists. |

Same-process instrumentation confirmed, in every run, that the test and implementation loaded from the respective disposable copy, `test_edits.apply_edits is text_edits.apply_edits`, and the executing code object matched that binding. There were **no setup failures**; the single failure was behavioral detection.

Concrete proposed assertions—**not executed or applied**:

- For forward application, add `self.assertEqual(result, "αQδεXYθ")` to the multiple-edits test. The overlap-only input cannot distinguish application order.
- For omitted overlap rejection, an overlapping call needs the existing overlap test’s exception assertion; stronger assertions on the nonoverlapping result cannot distinguish this fault.
- For caller-list mutation, save `before = edits.copy()` and assert `self.assertEqual(edits, before)` after success and after the expected exception. The overlap test would first need to retain its input list in a variable.

All original file bytes and modes were verified unchanged. Disposable copies were removed; no harness or report remains.
