I’ll use the con-artist skill to audit the three independent edits, verify the loaded code inside each native test process, and remove all temporary audit files afterward.

The selected tests check output values, including `maxsplit=0`, but use pure predicates and never check whether they were called. I’ll retain those assertions and add temporary regressions using a recording predicate and a locally raising predicate, with generator inputs and both `split_at` separator modes.

All three independent edits survived the original suite. Identical additional regressions detected each violation of your consumer contract.

Executed with `<TEMP>

```sh
python -B -m unittest -q \
  tests.test_more.SplitAtTests \
  tests.test_more.SplitBeforeTest \
  tests.test_more.SplitAfterTest
```

The augmented runs appended `test_consumer_audit.ZeroSplitContract`, adding six test methods without changing original assertions.

| Implementation | Original suite | Augmented suite |
|---|---|---|
| Correct | 13 tests, exit 0 | 19 tests, exit 0 |
| `split_at` fault | 13 tests, exit 0; survived | 19 tests, 4 subtest failures, exit 1 |
| `split_before` fault | 13 tests, exit 0; survived | 19 tests, 2 failures, exit 1 |
| `split_after` fault | 13 tests, exit 0; survived | 19 tests, 2 failures, exit 1 |

**Eight native executions total.** Each correct baseline ran once and was reused for the other two comparisons. No skips, timeouts, or truncated output.

The original zero-split assertions compare output using pure predicates. The additional regressions checked:

- Generator input produces the entire input as one group, including `[[]]` for empty input.
- A recording predicate receives no calls. Each fault instead recorded `[1, 0, 2]`, failing `self.assertEqual(calls, [])`.
- A locally raising predicate remains uncalled. Each fault triggered an explicit assertion failure reporting its invocation.
- Both `split_at` separator modes satisfy the contract.

Output and generator-exhaustion assertions passed before the recording assertions failed. Original ordinary-split controls remained green.

Inside every native test process, binding checks verified copied package/implementation/test paths, version `10.8.0`, public function identities, and selected test methods’ bindings to that package.

Whole-project integrity checks confirmed unchanged bytes and modes, including source, tests, license, and Git metadata. Installed resources were untouched; all owned scratch was removed. No report, harness, or permanent changes remain.

These findings establish sensitivity to the specified faults under your explicit `maxsplit=0` contract. They make no broader upstream callback-count or source-origin claim.
