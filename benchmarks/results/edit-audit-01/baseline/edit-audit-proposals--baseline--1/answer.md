I’ll read the contract, implementation, and tests, then run a correct copy and three isolated fault variants. I’ll also verify which `apply_edits` function each native test imports in the test process.

`test_multiple_edits` checks only the result’s type and length; it does not check the text or whether the caller’s list changed. `test_overlap` checks for the expected exception. I’ll run both tests against all four copies and record their function bindings and behavior without changing the test bodies.

Only `test_overlap` detects the omitted-overlap-check fault. The other five fault/test combinations pass.

Each test ran separately from its disposable copy root using `python3 -B -m unittest <selector> -v`. All test files remained byte-identical. Same-process instrumentation confirmed that `test_edits.apply_edits is text_edits.apply_edits`, that the executing code belonged to that function, and that both modules came from the intended copy.

The correct implementation passed both tests: `test_multiple_edits` returned `"αQδεXYθ"` without changing the list; `test_overlap` raised `ValueError("overlapping edits")` without changing the list. These baseline observations apply to all three comparisons.

| Independent fault | `test_multiple_edits` | `test_overlap` |
|---|---|---|
| Apply sorted edits forward using original offsets | **Survives:** returns incorrect `"αQδεζXY"`, but it remains a string of length 7, satisfying both assertions. | **Survives:** unchanged validation rejects overlap before application. |
| Remove overlap rejection, retain range validation | **Survives:** nonoverlapping input still produces correct `"αQδεXYθ"`. | **Detected:** returns `"aXf"`; `assertRaisesRegex` fails with `AssertionError: ValueError not raised`. |
| Sort caller list in place | **Survives:** correct output, but caller list becomes `[(1, 3, "Q"), (5, 7, "XY")]`; no assertion checks it. | **Survives:** expected exception occurs, but caller list becomes `[(1, 4, "X"), (3, 5, "Y")]`; no assertion checks preservation on failure. |

Faults were confined to `apply_edits`: changing application iteration direction, deleting only the overlap rejection, or replacing `sorted(...)` with `edits.sort(...)` and `ordered = edits`, respectively. No setup failures occurred. The single failing run was behavioral detection.

Concrete suggested assertions, **not added or executed**:

- In `test_multiple_edits`, add `self.assertEqual(result, "αQδεXYθ")` to distinguish forward application.
- Save `before = edits.copy()` before a call and assert `self.assertEqual(edits, before)` afterward to check preservation on success.
- In `test_overlap`, retain the input in an `edits` variable, snapshot it, and assert equality after the exception context to check preservation on failure.
- Detecting omitted overlap rejection requires overlapping input; the existing `test_overlap` already supplies it. Detecting forward application requires valid edits that reach application; an overlap-only call cannot distinguish it.

All disposable copies and instrumentation were removed. A before/after comparison confirmed original file bytes, modes, and project paths were preserved.
