I’ll use the con-artist skill to trace the manifest assertions, run the four native checks in disposable project-local copies, and change only the existing test file if the digest-loss fault survives.

The nonempty tests check only the returned count and file existence, so neither asserts that digests survive. Both fixture cases contain valid digests, including duplicate Unicode names. I’ll record the written JSON and loaded function in each test process, then add an exact comparison between the decoded manifest and the input records.

The original suite passed all three tests even with every digest erased. With the added JSON equality assertion, correct code still passes all three; faulty code fails both nonempty cases on the missing digests, while the empty control passes. Each process loaded its intended copied implementation. I’m applying the verified one-line test change and removing the scratch copies.

The existing tests missed digest loss. Added one assertion in [checks_manifest.py](project/checks_manifest.py#L7) comparing decoded JSON with the complete input records.

All four runs collected three native tests. Here `a×64` means exactly 64 lowercase `a` characters, likewise for `b` and `c`.

| Tests / implementation | Expected digests, both parametrizations | Observed digests | Native result | Exit |
|---|---|---|---|---|
| Original / correct | `[a×64]`; `[b×64, c×64]` | Identical | 3 passed | 0 |
| Original / faulty | `[a×64]`; `[b×64, c×64]` | `[""]`; `["", ""]` | 3 passed | 0 |
| Improved / correct | `[a×64]`; `[b×64, c×64]` | Identical | 3 passed | 0 |
| Improved / faulty | `[a×64]`; `[b×64, c×64]` | `[""]`; `["", ""]` | 2 failed, 1 passed | 1 |

Names, order and counts remained intact. Every empty control expected and observed `[]`, returning `0`. Both failures were equality assertions at line 7 showing empty digests against the expected values.

Used the documented interpreter and native command, adding only a temporary observation plugin:
`python -B -m pytest -vv -s -p no:cacheprovider checks_manifest.py -p audit_probe`.

Inside each test process, the plugin confirmed the test’s function binding matched `manifest.write_manifest`; module and function paths pointed into the corresponding disposable copy. Recorded implementation SHA-256 hashes were:

- Correct: `f8eaac61656a4ea2508fc566a049377a9cc6c8b31969a35b81d0952ce5974476`
- Faulty: `9b10709a2fd975d20d393badfcc3be0459405db736f77078ee7b91434881cc4b`

Only `checks_manifest.py` changed. Both parametrizations, empty control, fixtures and configuration were preserved. Verified all other original file bytes and modes unchanged; removed all owned scratch and instrumentation.
