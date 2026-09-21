I’ll use the con-artist skill to run the unchanged tests against correct code and three separate disposable variants, trace the implementation they load, and verify stronger assertions for any gaps. I’ll preserve the originals and remove the copies afterward.

`test_chain` checks only the result’s length and members; it checks neither prerequisite order nor input preservation. `test_cycle` checks the exception type and message, but not whether the input changed. I’ll run all six combinations and verify ordering and input-preservation assertions against correct and faulty code.

Only `test_cycle` detected the cycle-return regression. Neither native test detected caller-input mutation, and `test_chain` accepted reversed dependency order.

Ran these unchanged commands from each disposable copy root:

```sh
python3 -B -m unittest test_plan.PlanTests.test_chain -v
python3 -B -m unittest test_plan.PlanTests.test_cycle -v
```

Both correct-code tests passed (exit 0); those baselines are reused for all three comparisons.

| Independent fault in `plan` | `test_chain` | `test_cycle` |
|---|---|---|
| Return `order[::-1]` | **Survived**, exit 0. Returned `['ship', 'compile', 'fetch']`; length and set assertions ignore order. | **Survived**, exit 0. Raises before reaching the changed return. |
| Clear caller lists immediately after copying to working sets | **Survived**, exit 0. Correct schedule returned, but all prerequisite lists became empty. | **Survived**, exit 0. Expected exception still raised, but both caller lists became empty. |
| Return `order` when a cycle remains | **Survived**, exit 0. Acyclic input never reaches the changed branch. | **Detected**, exit 1. Returned `[]`; `assertRaisesRegex(ValueError, "dependency cycle")` failed with **“ValueError not raised.”** |

In-process tracing confirmed every native test called its copy’s `build_plan.py`, with the executed code object matching `test_plan.plan.__code__`. No import, syntax, or setup errors occurred; the failure was behavioral detection.

I verified these additional assertions in separate disposable tests without rewriting native test bodies:

- **Ordering:** assert `positions[parent] < positions[child]` for every dependency edge. Passed correct code; failed reversed code with `1 not less than 0` for `compile → ship`.
- **Input preservation:** deep-copy the graph before calling, then assert `graph == before`, both after success and after the expected cycle exception. Both passed correct code and failed the clearing variant on changed list contents.

Each additional run used `python3 -B -m unittest <selector> -v`; correct-code checks exited 0 and the corresponding faulty checks exited 1.

These results establish sensitivity to the specified faults, not the full contract. All original bytes and modes were verified unchanged. Disposable copies, instrumentation, and assertion probes were removed; no fixes or reports were retained.
