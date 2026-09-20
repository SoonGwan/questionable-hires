I’ll inspect the project’s test setup, compare correct and faulty implementations in disposable copies, and strengthen the existing test if it misses the digest loss.


The original suite passes all three tests even when every nonempty record has an empty digest. Its assertions check only the return count and file existence. I’ll add exact JSON equality to the existing parametrized test.

The temporary observer initially caused an unclosed-file warning; I fixed it and reran both checks successfully.


The existing tests missed digest loss. Added exact UTF-8 JSON equality in [checks_manifest.py](project/checks_manifest.py#L7), preserving both parametrizations and the empty control.

All four checks ran the documented full native command in disposable project-local copies. Here `a×64` means exactly 64 lowercase `a` characters, likewise for `b` and `c`.

| Tests / implementation | Expected digests by parametrization | Observed digests | Native result | Exit |
|---|---|---|---|---|
| Original / correct | `[a×64]`; `[b×64, c×64]` | Same | 3 passed | 0 |
| Original / faulty | `[a×64]`; `[b×64, c×64]` | `[""]`; `["", ""]` | 3 passed | 0 |
| Improved / correct | `[a×64]`; `[b×64, c×64]` | Same | 3 passed | 0 |
| Improved / faulty | `[a×64]`; `[b×64, c×64]` | `[""]`; `["", ""]` | 2 failed, 1 passed | 1 |

Names remained `release.zip` and duplicate `한글.zip`; order and counts were preserved. The empty control expected and observed `[]` in every run. Both improved failures were actual equality assertions at line 7 showing empty versus expected digests.

An observer inside each pytest process recorded matching `manifest.__file__` and function code paths under `.manifest-audit/{original,improved}-{correct,faulty}/manifest.py`, confirmed function identity, and captured source:
- Correct: `"sha256": item["sha256"]`, source SHA-256 `f8eaac61656a4ea2508fc566a049377a9cc6c8b31969a35b81d0952ce5974476`.
- Faulty: `"sha256": ""`, source SHA-256 `9b10709a2fd975d20d393badfcc3be0459405db736f77078ee7b91434881cc4b`.

Scratch was removed. Verified the original file set and all bytes/modes outside the allowed test edit remained unchanged.
