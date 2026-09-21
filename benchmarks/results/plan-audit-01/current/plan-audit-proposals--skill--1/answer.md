I’ll use the con-artist skill to run both unchanged tests against correct code and three separate mutations in disposable project copies, then remove the copies and verify the originals are unchanged.

`test_chain` checks length and membership, but not prerequisite order or input preservation. `test_cycle` checks the exception type and message, but not input preservation. Both import `plan` directly from `build_plan`; I’ll verify the copied module’s path in each native test process and run all six fault/test combinations.

Only `test_cycle` detected the partial-return regression. Reversed ordering and caller-input mutation survived both tests.

Each cell below represents an unchanged native test run from its disposable copy root:

```sh
python3 -B -m unittest test_plan.PlanTests.test_chain -v
python3 -B -m unittest test_plan.PlanTests.test_cycle -v
```

| Implementation | `test_chain` | `test_cycle` |
|---|---|---|
| Correct code | PASS, exit 0 | PASS, exit 0 |
| Reverse final returned order | PASS, exit 0 | PASS, exit 0 |
| Clear caller lists after copying into sets | PASS, exit 0 | PASS, exit 0 |
| Return partial order when a cycle remains | PASS, exit 0 | **FAIL, exit 1** |

The two correct-code observations serve as the reused baselines for all three faults. Each variant changed only `plan`, with faults kept separate.

`PYTHONVERBOSE=1` output from every native test process confirmed that it loaded `test_plan.py` and `build_plan.py` from the corresponding disposable copy. The tests directly import `plan` from that module. There were no setup, import, or syntax errors; the single failure was behavioral detection.

- **Reversed order:** A separate observation confirmed `['ship', 'compile', 'fetch']`. `test_chain` lines 8–9 check only length and membership, so both assertions pass. `test_cycle` raises before reaching the modified return.
- **Cleared lists:** Separate observations confirmed all caller lists became empty, while the chain schedule and cycle exception remained correct. Neither test checks input preservation; the cycle test passes its graph inline.
- **Partial cycle return:** The chain never reaches the changed branch. The cyclic input returns `[]`, causing `test_cycle`’s `assertRaisesRegex(ValueError, "dependency cycle")` to fail with **`AssertionError: ValueError not raised`**.

Concrete proposed assertions, **not applied or executed**:

- For this chain, add `self.assertEqual(result, ["fetch", "compile", "ship"])`. Its dependency order is unique.
- For input preservation, save `before = {name: parents[:] for name, parents in graph.items()}` before calling `plan`, then assert `self.assertEqual(graph, before)` afterward. Do this for both successful scheduling and the cycle case, retaining a named graph and checking it after the exception context.

These runs demonstrate specific coverage and gaps, not the full contract. All original bytes and modes were verified unchanged; disposable copies were removed, with no harness or report retained.
