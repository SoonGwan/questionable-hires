I’ll read the con-artist skill, then run the unchanged suite on correct code and the fault in disposable project-local copies, with binding checks inside each test process. I’ll add a regression assertion if the fault survives, then remove the scratch files and verify the project is unchanged.

The four existing tests exercise environment and explicit overrides separately, so none compares their precedence when both supply a value. I’ll test the reversed order, then add one assertion with conflicting values in both layers to check that it detects the fault.

The reversed-precedence fault **survives the original suite**. Existing tests never supply conflicting environment and override values.

| Suite | Code | Native result | Exit |
|---|---|---|---|
| Original unchanged | Correct | 4 passed | 0 |
| Original unchanged | Reversed precedence | 4 passed; fault survived | 0 |
| With regression | Correct | 5 passed | 0 |
| With regression | Reversed precedence | 4 passed, 1 assertion failure | 1 |

Original assertions returned matching actual/expected `retries` values in both runs: defaults `3`, environment `4`, override `5`, absent override `3`.

Added and verified in disposable copies, preserving every existing assertion:

```python
def test_override_beats_environment(self):
    self.assertEqual(
        resolve({'retries': 3}, {'retries': 4}, {'retries': 5}),
        {'retries': 5},
    )
```

Correct code returned `{'retries': 5}`; the fault returned `{'retries': 4}`, causing the intended assertion failure.

All four executions used the supplied Python and native `unittest` entry point through `runpy`, with `-v test_settings`. Each actual test process verified copy-local module paths, `test_settings.resolve is settings.resolve`, and the resolver’s code path. No observations were reused; no import, setup, or empty-suite failures occurred.

All original file bytes and modes, Git HEAD/index, and skill resources remained unchanged. Scratch was removed; no harness or report remains. This establishes detection of the supplied precedence fault, not coverage of the entire contract.
