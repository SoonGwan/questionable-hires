I’ll inspect the implementation and native tests, run each isolated fault in a disposable copy, and verify stronger assertions for any gaps. I’ll then remove the copies and check that all original bytes and modes are unchanged.

The chain test checks length and membership but not prerequisite order. The cycle test checks the exception but never inspects the input afterward. I’ll run all six fault/test combinations and add disposable assertions for ordering and input preservation on both success and cycle failure.

The native tests detected only regression 3. Ordering and caller-input mutation survived.

Each fault occupied a separate disposable copy, changing only `build_plan.plan`:

1. Replace the final return with `return order[::-1]`.
2. After constructing internal sets, call `clear()` on every caller-owned prerequisite list.
3. Replace the cycle exception with `return order`.

Native test files remained byte-identical. In every copy, import checks confirmed `test_plan.plan is build_plan.plan` and that both modules resolved inside that copy.

All tests ran from their respective copy roots using:
```text
python3 -B -m unittest <selector> -v
```

| Implementation | `test_plan.PlanTests.test_chain` | `test_plan.PlanTests.test_cycle` |
|---|---|---|
| Correct | PASS | PASS |
| Reverse order | PASS — survives | PASS — cycle exception unchanged |
| Clear caller lists | PASS — survives | PASS — survives |
| Return partial order on cycle | PASS — acyclic behavior unchanged | FAIL — `ValueError not raised` |

The two correct-code observations were reused across all three comparisons. Passes exited 0; the failure exited 1. There were no setup or import errors.

`test_chain` checks only length and membership, so the reversed result `["ship", "compile", "fetch"]` passes. Neither native test checks input preservation. `test_cycle` detects regression 3 through `assertRaisesRegex(ValueError, "dependency cycle")`; the faulty implementation returns `[]` for its fully cyclic graph.

I also executed three stronger tests, without rewriting native test bodies:

| Added assertion and context | Correct | Corresponding fault |
|---|---|---|
| Chain: `self.assertEqual(result, ["fetch", "compile", "ship"])` | PASS | Reverse: FAIL at this assertion |
| Chain, after successful scheduling: `self.assertEqual(graph, before)` | PASS | Clear lists: FAIL at this assertion |
| Cycle, after catching the expected exception: `self.assertEqual(graph, before)` | PASS | Clear lists: FAIL at this assertion |

For both preservation tests, the snapshot copied list contents before calling `plan`:
```python
before = {name: parents[:] for name, parents in graph.items()}
```

The success test first verified the correct schedule. The cycle test first verified `ValueError` with `^dependency cycle$`. Thus, both mutation failures occurred at the preservation assertion after the expected scheduling or exception behavior succeeded. Exact ordering is appropriate for this chain because its valid order is unique.

These results establish specific coverage gaps, not full-contract correctness. All disposable copies and extra tests were removed; a before/after comparison verified unchanged original file bytes, modes, and project inventory.
