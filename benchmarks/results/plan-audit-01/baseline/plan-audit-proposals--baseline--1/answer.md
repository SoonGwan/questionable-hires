I’ll inspect the implementation and native tests, then run each isolated fault in a disposable copy and verify that the original files remain unchanged.

Only regression **(3) is detected**, by `test_cycle`. The other five fault/test combinations pass.

Ran these unchanged native tests from each disposable copy’s root:

```sh
python3 -B -m unittest test_plan.PlanTests.test_chain -v
python3 -B -m unittest test_plan.PlanTests.test_cycle -v
```

Both correct-code tests passed (exit 0). Those two baseline observations are reused for all three comparisons.

| Isolated change inside `plan` | `test_chain` | `test_cycle` |
|---|---|---|
| (1) Final return becomes `return order[::-1]` | PASS, exit 0 — survives | PASS, exit 0 — survives |
| (2) After constructing internal sets, call `clear()` on every caller-owned prerequisite list | PASS, exit 0 — survives | PASS, exit 0 — survives |
| (3) Replace cycle exception with `return order` | PASS, exit 0 — survives | **FAIL, exit 1 — detected** |

The assertions explain these outcomes:

- **Reversed order:** `test_chain` checks only length and membership. `["ship", "compile", "fetch"]` satisfies both despite violating prerequisite ordering. `test_cycle` still raises before reaching the reversed return.
- **Cleared input lists:** The internal sets already contain the prerequisites, so scheduling and cycle detection remain intact. Neither test checks input preservation; the cycle test passes an inline dictionary that it never inspects afterward.
- **Partial return on a cycle:** The acyclic chain is unaffected. For the cyclic input, `plan` returns `[]`; `assertRaisesRegex(ValueError, "dependency cycle")` fails with **`AssertionError: ValueError not raised`**. This is behavioral detection, not a setup error.

Import tracing during every native run identified that copy’s `test_plan.py` and `build_plan.py`. A separate binding check in each copy confirmed `test_plan.plan is build_plan.plan` and the function’s local source path. All eight runs executed their selected test; none had setup/import errors.

Concrete assertions to add later, **not implemented here**:

- For this chain, assert `result == ["fetch", "compile", "ship"]`. For general DAGs, assert every prerequisite’s result index is smaller than its dependent’s, alongside membership and uniqueness checks.
- Snapshot inputs using `{name: parents[:] for name, parents in graph.items()}` and assert equality after successful scheduling **and after catching a cycle exception**.
- Add a graph containing an independent task plus a cycle, and assert it still raises; this covers rejection after a nonempty partial schedule.
- If exact exception text matters, assert `str(exception) == "dependency cycle"`; the existing regex allows additional text.

These tests do not establish the full contract. All original file bytes and modes were verified unchanged; disposable copies were removed, with no harness or report retained.
