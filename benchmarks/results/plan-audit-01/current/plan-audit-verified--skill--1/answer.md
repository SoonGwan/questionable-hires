I’ll use the con-artist skill to run each fault separately against the unchanged native tests, then verify stronger assertions in disposable copies. I’ll check which implementation the test processes load and preserve all original files.



`test_chain` checks only length and membership, so it appears unable to detect reversed ordering or mutated input. `test_cycle` checks the exception type and message but never inspects input afterward. I’ll verify those gaps with native runs, then test prerequisite ordering and input preservation on both successful and failing calls.



The native tests detect the suppressed cycle exception, but miss reversed ordering and caller-input mutation.

Each run used the following command from its disposable copy root:

```sh
python3 -B -m unittest <selector> -v
```

In-process tracing confirmed that each test called its copy’s `build_plan.py:plan`, recording the implementation path, source hash, inputs, and outcome. Native test files remained byte-identical. Each faulty implementation changed only `plan`, with faults kept separate.

Both correct-code native tests passed (exit 0); those baselines are reused across the six comparisons below.

| Independent fault | `test_plan.PlanTests.test_chain` | `test_plan.PlanTests.test_cycle` |
|---|---|---|
| Reverse complete acyclic order | **PASS, 0 — missed.** Returned `['ship', 'compile', 'fetch']`; length and set assertions still passed. | **PASS, 0.** Cycle still raised; reversal was not reached. |
| Clear caller lists after copying into working sets | **PASS, 0 — missed.** Correct schedule returned, but every caller list became empty. | **PASS, 0 — missed.** Expected exception raised, but caller input became `{'a': [], 'b': []}`. |
| Return partial order when a cycle remains | **PASS, 0.** Acyclic schedule unchanged; faulty branch was not reached. | **FAIL, 1 — detected.** Returned `[]`; `assertRaisesRegex` failed with `ValueError not raised`. |

All runs executed one test. There were no setup, import, or syntax errors; the failure above was behavioral detection.

I also executed three stronger tests, added only to disposable copies:

| Added selector under `test_stronger.StrongTests` | Concrete distinguishing assertion | Correct | Corresponding faulty |
|---|---|---|---|
| `test_prerequisite_order` | From a pre-call graph snapshot, assert `positions[parent] < positions[task]` for every dependency edge. | **PASS, 0** | Reverse: **FAIL, 1**, `1 not less than 0 : compile must precede ship`. |
| `test_preserves_chain_input` | Save `before = deepcopy(graph)`; after `plan(graph)`, assert `graph == before`. | **PASS, 0** | Clear: **FAIL, 1**, prerequisite lists were empty. |
| `test_preserves_cycle_input` | Save the same snapshot; after the expected exception is caught by `assertRaisesRegex`, assert `graph == before`. | **PASS, 0** | Clear: **FAIL, 1**, both prerequisite lists were empty despite the expected exception. |

The ordering assertion permits arbitrary ordering among independent tasks. Preservation tests also included list identity and alias-content checks, but the faulty runs failed first at snapshot equality; those later checks have no independently demonstrated detection result.

These outcomes establish sensitivity to the specified faults on these fixtures, not the full contract. All disposable copies were removed. A before/after snapshot confirmed unchanged original paths, file bytes, and modes, including Git metadata; no harness, report, or fixes remain.
