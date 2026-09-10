I’ll use the con-artist skill to trace the test’s assertions and run a lost-write mutation in a disposable copy inside this project, preserving the original code.

**The test catches the lost write.**

Executed in a disposable copy inside this project:

```sh
python3 -B -m unittest -v test_service.SaveTests.test_save
```

- **Baseline:** passed, exit 0.
- **Mutation:** removed `store.append(record)`, preserving `return {'ok': True}`.
- **Mutant:** failed, exit 1: `[] != ['record']`.

The success assertion alone would miss the fault. The existing `self.assertEqual(store, ['record'])` checks the actual list contents and detects it; no stronger assertion is needed for this scenario.

The disposable copy was removed. Original production code and test remain byte-for-byte unchanged.
