I’ll use the con-artist skill to run the three faults separately in disposable copies, verify the test-process bindings, and check stronger assertions against correct and faulty code. I’ll preserve the originals and remove the copies afterward.

`test_multiple_edits` checks only type and length, so it may miss incorrect characters and caller-list mutation. `test_overlap` checks the exception message but never inspects the list afterward. I’ll test those gaps and trace the function binding inside each native unittest process.

The first baseline passed, but Python did not load the startup instrumentation, leaving the required binding evidence missing. I’ve discarded that run as incomplete and removed its copy. I’ll rerun with the disposable copy explicitly on `PYTHONPATH`; this was a setup issue, not fault detection.

All six requested fault/test combinations are complete: only `test_overlap` detects the missing overlap check. The stronger assertions pass on correct code and fail for the intended faults: wrong output, list mutation after success, and list mutation before overlap rejection. A supplementary `test_controls` run also detected forward application through its deletion example; I’ll finish the other control runs.

The two requested tests detect only omitted overlap rejection. They miss forward application and caller-list mutation.

Each fault was confined to `apply_edits` in a separate disposable copy:

- **Forward:** replace `reversed(ordered)` with `ordered`.
- **No overlap check:** remove only overlap rejection; retain range validation.
- **In-place sort:** replace `sorted(...)` with `edits.sort(...)` and `ordered = edits`.

Original test bodies remained byte-identical.

| Implementation | `test_multiple_edits` | `test_overlap` |
|---|---|---|
| Correct baseline | PASS, exit 0 | PASS, exit 0 |
| Forward | PASS: incorrect `"αQδεζXY"` still has length 7 | PASS: rejection happens before application |
| No overlap check | PASS: input has no overlap | **FAIL**, exit 1: `ValueError not raised`; returned `"aXf"` |
| In-place sort | PASS: correct output, caller list reordered | PASS: expected exception, caller list reordered |

The two correct baseline observations are reused across the three comparisons.

Stronger assertions were **actually executed** in disposable test modules:

| Assertion/check | Correct | Corresponding fault |
|---|---|---|
| Exact original-coordinate output equals `"αQδεXYθ"` | PASS | Forward: FAIL, got `"αQδεζXY"` |
| Overlap raises `ValueError` matching `^overlapping edits$` | PASS | No overlap check: FAIL, no exception |
| Save `before = list(edits)`; assert exact output, then `edits == before` | PASS | In-place: FAIL at list equality |
| Save overlap input; assert expected rejection, then `edits == before` | PASS | In-place: FAIL at list equality |

These are verified improvements for the demonstrated gaps. The preservation checks used the existing unsorted inputs, so sorting changed their order observably.

All runs used, from the relevant copy root:

```sh
python3 -B -m unittest <selector> -v
```

Selectors were `test_edits.EditTests.{test_multiple_edits,test_overlap}` and `test_contract_audit.ContractTests.{test_exact_original_coordinates,test_overlap_rejection,test_caller_preserved_success,test_caller_preserved_overlap}`, each run individually.

Same-process tracing recorded copied module paths and verified both `test_edits.apply_edits is text_edits.apply_edits` and identity with the executing code object. Equivalent checks covered the added assertions.

One initial baseline lacked startup instrumentation and was excluded as incomplete setup evidence. Explicitly setting `PYTHONPATH` to the copy fixed this. All reported detecting failures were behavioral assertion failures, not import or runner errors.

Supplementary `test_controls` passed on correct, no-overlap, and in-place copies, including invalid-range rejection. It independently detected forward application (`"βZ" != "Z"`).

All disposable copies were removed. Whole-project before/after checks confirmed original file bytes and modes were preserved; no harness or report remains.
