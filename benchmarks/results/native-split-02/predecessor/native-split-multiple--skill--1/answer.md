I’ll use the con-artist skill to run the selected native tests against each isolated edit, then verify focused regressions for the consumer contract if the original tests miss it. I’ll check bindings inside each test process and remove all audit scratch afterward.

The selected tests check output values at `maxsplit=0`, but use predicates whose extra calls have no observable effect. I’ll add temporary regressions using a local call log and a raising callable, with generator inputs, empty inputs, and both `split_at` separator settings. The original tests will remain unchanged and provide the ordinary-split controls.

All three independent edits **survived the original tests**. Identical added regressions detected each violation of your consumer contract.

Executed in isolated copies using:
```sh
<TEMP> -B -m unittest -v \
  tests.test_more.SplitAtTests \
  tests.test_more.SplitBeforeTest \
  tests.test_more.SplitAfterTest
```

The augmented runs appended `test_consumer_contract.ZeroSplitContract`.

| Code | Original suite | Original + regressions |
|---|---|---|
| Correct | 13 tests, exit 0 | 16 tests, exit 0 |
| `split_at` edit | 13 tests, exit 0 — survived | 16 tests, 4 subtest failures, exit 1 |
| `split_before` edit | 13 tests, exit 0 — survived | 16 tests, 2 subtest failures, exit 1 |
| `split_after` edit | 13 tests, exit 0 — survived | 16 tests, 2 subtest failures, exit 1 |

**Eight native executions total.** Each correct baseline ran once and was reused for the remaining comparisons. No skips or timeouts.

The original assertions compare output values; their predicates do not expose extra calls. The added regressions used generator inputs yielding `[1, 0, 2]` or nothing, with deterministic local predicates:

- A logging predicate preserved output `[[1, 0, 2]]` and generator consumption, then failed `self.assertEqual(calls, [])`: actual calls were `[1, 0, 2]`.
- A raising predicate triggered an explicit assertion failure: `maxsplit=0 invoked raising predicate: local predicate witness`.

Both `split_at` separator settings were checked. Empty inputs returned `[[]]`. All unchanged ordinary-split tests passed, including in augmented faulty runs.

Every native test process verified copied package, implementation, and test paths/hashes; public function identity against `more_itertools.more`; and selected test methods’ `mi` bindings. Augmented processes also verified the regression binding.

This establishes sensitivity to the three specified faults under your explicit `maxsplit=0` contract. It makes no broader upstream callback-count guarantee.

The project inventory confirmed unchanged bytes/modes, including source, tests, LICENSE, and Git metadata. Installed resources were not modified. All owned scratch was removed; no report, harness, fix, or permanent test change remains.
