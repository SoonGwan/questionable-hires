I’ll check the supplied files, run the selected native suite on the correct and independently modified copies, and add identical focused regressions if needed. I’ll verify bindings inside each test process and remove all scratch files afterward.

The selected tests check `maxsplit=0` output values, but don’t detect predicate calls. I’ll use a local call log and a callable that raises as witnesses, alongside checks for empty input, generator consumption, separator retention, and ordinary splits.

The supplied `split_at` edit violates the consumer contract but survives the original selected suite.

All four executions used `<TEMP> -B -m unittest -v`.

| Code | Native suite | Tests | Result | Exit |
|---|---|---:|---|---:|
| Correct | Original three class selectors | 13 | Passed | 0 |
| Faulty `split_at` | Same unchanged selectors/assertions | 13 | Survived | 0 |
| Correct | Focused regressions | 5 | Passed | 0 |
| Faulty `split_at` | Identical focused regressions | 5 | 4 subtest assertion failures | 1 |

The failures occurred with both separator-retention settings:

- A local recording predicate received `[1, 2, 3]`; the assertion required zero calls.
- A local raising predicate produced `RuntimeError` instead of returning `[[1, 2, 3]]`.

Output-only checks, empty input, generator consumption, ordinary unlimited/one-split behavior, and neighboring `split_before`/`split_after` checks passed.

Each native test process verified version `10.8.0`, copy-specific package/implementation/test paths and hashes, exported function identities, implementation code paths, and test bindings before running. These were four actual executions; no reused observation was counted as another run.

This establishes the explicit `maxsplit=0` consumer requirement, not arbitrary callback-count guarantees in other modes or an upstream documentation promise.

Original source/tests/license bytes and modes, Git HEAD/index, and the project tree were verified unchanged. Installed resources were untouched. All owned scratch was removed; no fix, harness, or report remains.
