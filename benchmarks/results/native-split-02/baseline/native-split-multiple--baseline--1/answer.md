I’ll run the selected tests on the correct source and three independent faulty copies, verify bindings inside each test process, and check the consumer contract with identical additional regressions. I’ll remove the scratch files and verify the supplied tree is unchanged.


The selected tests check output at `maxsplit=0`, but their predicates have no observable effects. I’ll add separate native tests with a recording callable and a raising callable, plus generator-input, empty-input, separator-retention, and ordinary-split checks.


All three isolated edits violate the consumer contract, but survive the unchanged original suite.

Executed with `<TEMP> -B -m unittest -v`, using the exact requested selectors for original tests and identical additional regressions for every copy:

| Copy | Original suite | Additional regressions |
|---|---|---|
| Correct | 13 tests passed; exit 0 | 12 tests passed; exit 0 |
| `split_at` faulty | 13 tests passed; exit 0 | 12 tests; 4 subtest failures; exit 1 |
| `split_before` faulty | 13 tests passed; exit 0 | 12 tests; 2 failures; exit 1 |
| `split_after` faulty | 13 tests passed; exit 0 | 12 tests; 2 failures; exit 1 |

Eight native processes ran. The single correct observation for each suite is reused across all three comparisons.

The detecting assertions used generator input `[1, 2, 3]`:
- A recording predicate preserved output `[[1, 2, 3]]`, but recorded `[1, 2, 3]` instead of the required `[]`.
- A raising predicate triggered an explicit assertion failure because its local `RuntimeError` escaped.

`split_at` failed both checks with default separator handling and `keep_separator=True`. Empty-input and ordinary-split checks (`maxsplit=-1, 1, 2`) passed everywhere.

Inside every native test process, checks confirmed package/version, implementation path and hash, exported-function identity, test paths, and test globals bound to that copy.

These results establish the specified zero-split consumer contract violation, without asserting upstream guarantees about callback counts in other modes.

Cleanup completed. Original source/tests/license bytes and modes, and Git metadata including HEAD/index, remained unchanged. Installed resources were untouched; no scratch, harness, report, or production changes remain.
