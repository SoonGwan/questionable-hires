I’ll use the con-artist skill to run each fault separately in disposable copies, verify test-process bindings, and check stronger assertions. I’ll preserve the original files and remove the copies afterward.


The native tests detect omitted overlap rejection, but miss forward application and caller-list mutation.

Each fault was confined to `apply_edits` in a separate disposable copy:

1. Changed `reversed(ordered)` to `ordered`.
2. Removed only overlap rejection; retained range validation.
3. Replaced `sorted(...)` with `edits.sort(...)` and `ordered = edits`.

Original test bodies remained byte-identical.

| Implementation | `test_multiple_edits` | `test_overlap` |
|---|---|---|
| Correct | PASS | PASS |
| Forward application | PASS — survives | PASS — validation rejects before application |
| Omitted overlap rejection | PASS — input has no overlap | **FAIL — `ValueError not raised`** |
| In-place sorting | PASS — survives | PASS — survives |

The two correct-code results serve as shared baselines for all six comparisons.

`test_multiple_edits` checks only string type and length 7. Forward application returned **`αQδεζXY`**, whereas the contract requires **`αQδεXYθ`**; both satisfy those assertions. In-place sorting produced the correct output but reordered the caller’s list.

`test_overlap` detects missing rejection through `assertRaisesRegex(ValueError, "overlapping edits")`: that mutant returned `aXf`. In-place sorting still raised the expected exception, but changed the caller’s list before raising; the test never checks it.

I also **executed** these stronger assertions in disposable tests:

| Assertion | Correct | Corresponding fault |
|---|---|---|
| Exact output equals `"αQδεXYθ"` | PASS | Forward: FAIL, wrong text |
| Successful call: exact output, then `assertEqual(edits, before)` | PASS | In-place: FAIL, reordered list |
| Overlap raises `ValueError` matching `^overlapping edits$` | PASS | Omitted rejection: FAIL, no exception |
| After caught overlap rejection: `assertEqual(edits, before)` | PASS | In-place: FAIL, reordered list |

Here, `before = edits.copy()` precedes each call, using the original tests’ unsorted inputs. These are verified improvements suitable for the existing tests.

All 16 runs used this command form from the corresponding copy root:

```sh
python3 -B -m unittest <selector> -v
```

Selectors were the two requested native methods and four disposable `test_contract.ContractTests` methods. Same-process tracing verified the copied module path, the test module’s imported `apply_edits` identity, and the executing function’s code identity. Every failure was an intended assertion failure with exit 1; passes exited 0. There were no setup failures.

All disposable files were removed. Whole-project comparison confirmed unchanged original file bytes and modes, including Git metadata, with no added paths.
