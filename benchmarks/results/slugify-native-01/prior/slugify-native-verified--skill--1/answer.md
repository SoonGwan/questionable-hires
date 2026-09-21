I’m using the con-artist skill to check the six fault/test combinations and verify assertions that close any gaps, using disposable copies only.


The selected tests use the default separator and leave `save_order=False`, so neither exercises those options. `test_max_length` does directly check truncation. Two existing upstream tests provide the requested witnesses: `test_custom_separator` checks dots, and `test_save_order` checks that truncation stops before `three` even though the later word `four` would fit.


Only `test_max_length` detected a requested regression.

| Independent fault | `test_non_word_characters` | `test_max_length` |
|---|---|---|
| Omit custom separator conversion | PASS — survives | PASS — survives |
| Force `save_order=False` | PASS — survives | PASS — survives |
| Omit max-length truncation | PASS — survives | FAIL — detected |

Both selected tests passed on correct code. That single matching baseline was reused for faults 2 and 3.

`test_non_word_characters` checks `"this-is-a-test"` without requesting truncation or a custom separator. `test_max_length` also uses the default separator and ordering options. It detects omitted truncation at `test.py:65`: expected `"jaja-lol"`, received `"jaja-lol-mememeoo-a"`. Its second assertion is not reached under that fault.

Verified the gaps using unchanged upstream witnesses:

- `test_custom_separator`: **correct PASS; separator fault FAIL**. With `separator="."`, the assertion expects `"jaja.lol.mememeoo.a"`; faulty code returns `"jaja-lol-mememeoo-a"`.
- `test_save_order`: **correct PASS; ordering fault FAIL** at `test.py:118`. For `"one two three four five"`, `max_length=12`, `word_boundary=True`, `save_order=True`, it expects `"one-two"`; faulty code returns `"one-two-four"`. Earlier `"three"` cannot fit, but later `"four"` can.

All executions used the configured interpreter with `-B -m unittest <selectors> -v` from fresh project-local copy roots. Same-process checks verified copied imports and the native test functions’ `slugify` binding. Failures were native assertion failures; no setup errors occurred.

Faults remained independent and confined to `slugify()`. All original bytes and modes were preserved, all test bodies stayed unchanged, and all owned scratch was removed.
