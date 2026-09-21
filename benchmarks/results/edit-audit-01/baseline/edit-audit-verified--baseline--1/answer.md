I’ll read the contract, implementation, and tests, then run each isolated fault against both native tests and stronger assertions in disposable copies. I’ll also verify the function binding used by the tests and check that all original files remain unchanged.



The multiple-edits test checks only the result’s type and length, so it may miss incorrect output and caller-list mutation. The overlap test checks rejection but not whether rejection leaves the list unchanged. I’ll test those gaps with exact-output and list-preservation assertions, including preservation after overlap rejection.



The native tests detect only the omitted-overlap fault among the six requested combinations.

| Implementation | `test_multiple_edits` | `test_overlap` |
|---|---|---|
| Correct baseline | PASS | PASS |
| Forward application | PASS — fault survives | PASS — fault survives |
| No overlap rejection | PASS — fault survives | **FAIL — detected** |
| In-place sorting | PASS — fault survives | PASS — fault survives |

The correct baseline observations are reused for all three comparisons. Each fault was independently confined to `apply_edits`: forward iteration, removal of only the overlap check, or replacement of `sorted(...)` with `edits.sort(...)` and `ordered = edits`.

- **Forward application:** produces `"αQδεζXY"` instead of `"αQδεXYθ"`. Both are seven-character strings, satisfying the native type and length assertions. Overlap validation still rejects before application.
- **No overlap rejection:** the multiple-edits input does not overlap. The overlap test fails behaviorally with `AssertionError: ValueError not raised`. Range validation remains intact; the native controls passed.
- **In-place sorting:** output and overlap rejection remain correct, but both inputs are reordered. Neither native test asserts caller-list preservation.

I also **executed** these stronger assertions in disposable copies:

| Assertion | Correct | Corresponding fault |
|---|---|---|
| Exact output equals `"αQδεXYθ"` | PASS | Forward: **FAIL**, actual `"αQδεζXY"` |
| Successful call preserves `edits == before` | PASS | In-place: **FAIL**, list reordered |
| Overlap raises `ValueError` matching `^overlapping edits$` | PASS | No-overlap: **FAIL**, no exception |
| After expected overlap rejection, `edits == before` | PASS | In-place: **FAIL**, list reordered |

For preservation checks, `before = edits.copy()` was captured before calling, using the original unsorted inputs. These are concrete, verified additions recommended for the native tests. Against the no-overlap variant, the rejection-and-preservation test stops at the missing exception; it does not establish preservation afterward.

Every invocation used `python3 -B -m unittest <selector> -v` from its copy root. Same-process instrumentation verified the copied module path, the function’s code path, and `test_edits.apply_edits is text_edits.apply_edits`; source hashes matched each intended variant. Native test bodies remained unchanged. There were **no setup failures**.

An additional controls run detected forward application (`"βZ"` versus `"Z"`); correct and both other variants passed.

All disposable copies were removed. Before/after snapshots confirmed original file bytes and modes were preserved, with no harness or report retained.
