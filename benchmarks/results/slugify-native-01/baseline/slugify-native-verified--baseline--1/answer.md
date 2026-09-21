I’ll run the two selected tests against independent fault copies, verify the imported function binding in each test process, and check any gaps with targeted assertions in disposable copies. I’ll then remove the copies and verify the original files are unchanged.

The selected tests use the default separator and never request `save_order=True`, so they appear to leave both regressions uncovered. The upstream `test_custom_separator` and `test_save_order` provide suitable witnesses: the latter checks a 12-character limit where `three` cannot fit after `one-two`, but the later word `four` can. I’ll run these alongside the six required fault/test combinations.

Only `test_max_length` detected a regression: omitted truncation.

| Independent implementation | `test_non_word_characters` | `test_max_length` |
|---|---|---|
| Correct control | PASS | PASS |
| Omit custom separator conversion | PASS—gap | PASS—gap |
| Force `save_order=False` | PASS—gap | PASS—gap |
| Omit max-length truncation | PASS—gap | FAIL—detected |

`test_non_word_characters` requests neither a custom separator nor truncation. `test_max_length` uses the default separator and default `save_order=False`, leaving those faults undetected. Against omitted truncation, its first assertion expected `jaja-lol` but received `jaja-lol-mememeoo-a`; the second assertion was not reached.

Both surviving feature gaps were verified using unchanged upstream witnesses:

- **`test_custom_separator`:** passed correct code; failed the separator fault, expecting `jaja.lol.mememeoo.a` but receiving `jaja-lol-mememeoo-a`.
- **`test_save_order`:** passed correct code; failed the order fault at `max_length=12, word_boundary=True, save_order=True`, expecting `one-two` but receiving `one-two-four`. The earlier word `three` cannot fit, while the later, shorter `four` can.

The two selected correct-code observations were reused across all three fault comparisons. The passing `test_max_length` control also supplies the matching truncation-detection control.

All 12 test outcomes ran with the configured interpreter using `-B -m unittest <selectors> -v` from independent copy roots. Each process verified that `test.slugify` was bound to its copied implementation. Failures were native assertion failures, with no setup errors. All upstream test bodies remained unchanged; scratch was removed, and original file bytes, modes, and tree entries were verified unchanged.
