I’ll inspect the test and write path, then run an isolated mutation to see whether the test detects a lost write.

The test checks only the returned `ok` flag; it never checks the store. I’ll replace `save` in the test’s namespace with a function that reports success without writing, then run the same test. This keeps production code untouched.

The test **does not catch a lost write**. It checks only `ok`, not whether the record was stored.

Demonstrated with an isolated, in-memory replacement that returns `{'ok': True}` without appending:

- Original implementation: test passes.
- Lost-write mutation: same test still passes, with the store empty.
- An assertion that the store equals `['record']` detects the mutation.

To close the gap, retain the list and assert its contents after calling `save`.

The replacement was restored, production code was untouched, and the working tree is clean.
