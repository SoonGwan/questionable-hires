I’ll use the con-artist skill to run the six native test/fault combinations in disposable copies, then verify stronger ordering and input-preservation assertions against correct and faulty code. I’ll check what each test process actually loads and preserve all original files.



The native chain test checks only length and membership; the cycle test checks the exception and message. My first correct-code run passed, but the provenance hook didn’t load, so it doesn’t establish which implementation ran. I’ll fix that setup and rerun with the hook loaded from each disposable copy.



The native tests detect regression 3, but miss reversed scheduling and caller-input mutation.

Each fault changed only `build_plan.plan` in a separate disposable copy:

1. Final return changed to `return list(reversed(order))`.
2. Each caller-owned list cleared immediately after creating internal sets.
3. Cycle exception replaced with `return order`.

The native test file remained byte-identical.

| Implementation | `test_chain` | `test_cycle` |
|---|---|---|
| Correct | PASS (0) | PASS (0) |
| Reverse order | PASS (0): gap | PASS (0): reversal not reached |
| Clear caller lists | PASS (0): gap | PASS (0): gap |
| Return partial order on cycle | PASS (0): cycle branch not reached | FAIL (1): `ValueError not raised` |

The two correct-code observations are reused across all three fault comparisons.

`test_chain` asserts only length and membership. Thus `['ship', 'compile', 'fetch']` passes despite violating dependency order. Neither native test checks input preservation: clearing the lists preserves the chain’s returned schedule and the cycle’s expected exception. `test_cycle` detects regression 3 through `assertRaisesRegex(ValueError, "dependency cycle")`; the faulty implementation returns `[]`.

I also **executed** three stronger tests, using the same chain and cycle inputs:

| Added assertion | Correct | Corresponding fault |
|---|---|---|
| `self.assertEqual(result, ["fetch", "compile", "ship"])` | PASS (0) | Reverse: FAIL (1), reversed list |
| Deep-copy chain before calling; `self.assertEqual(graph, before)` afterward | PASS (0) | Clear lists: FAIL (1), prerequisites erased |
| Deep-copy cycle; retain `assertRaisesRegex`; compare graph afterward | PASS (0) | Clear lists: FAIL (1), prerequisites erased |

For the last test, both implementations raised the expected exception; the faulty copy failed specifically at the subsequent preservation assertion. Exact schedule equality is appropriate for this chain because its valid order is unique.

All 14 verified executions ran from their respective copy roots using:

```sh
python3 -B -m unittest <selector> -v
```

Selectors were the two requested native tests and `test_contract_audit.ContractTests.{test_chain_order,test_chain_input_preserved,test_cycle_input_preserved}`. An in-process trace confirmed each actual test called its copy’s `build_plan.py`, recording inputs, results, and exceptions.

An initial baseline passed without loading the provenance hook. That was an instrumentation setup failure, not behavioral detection; it was excluded and rerun with `PYTHONPATH` pointing to the copy root. All reported failures were assertion failures, with no unittest errors.

Original file hashes and modes were preserved. All disposable copies and added tests were removed; no harness or report remains. These results establish sensitivity to the specified faults, not proof of the full contract.
