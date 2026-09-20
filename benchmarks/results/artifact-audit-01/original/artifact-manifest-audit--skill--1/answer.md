I’m using the con-artist skill to inspect the native assertions, run the specified digest fault in disposable copies, and strengthen only the existing test file if needed.

The nonempty tests check only the return count and file existence; they never read the stored digests. The native suite has two nonempty cases and one empty control. I’ll run all three in each copy and capture the actual JSON plus the implementation executed by each test process.

The original suite passed with every digest empty. The strengthened tests pass on correct code and fail both nonempty cases on the exact digest mismatch; the empty control still passes. I’ll apply the verified one-line assertion, remove the scratch copies, and check that all other file bytes and modes are unchanged.

The original tests missed digest loss. Added exact decoded-JSON equality in [checks_manifest.py](project/checks_manifest.py#L7).

Here `a×64`, `b×64`, and `c×64` mean those characters repeated 64 times. Expected digests were `[a×64]` for `release.zip` and `[b×64, c×64]` for the duplicate `한글.zip` records.

| Native check | Observed digests, respectively | Results | Exit |
|---|---|---|---|
| Original / correct | `[a×64]`; `[b×64, c×64]` | 3 passed | 0 |
| Original / faulty | `[""]`; `["", ""]` | 3 passed | 0 |
| Improved / correct | `[a×64]`; `[b×64, c×64]` | 3 passed | 0 |
| Improved / faulty | `[""]`; `["", ""]` | 2 failed, 1 passed | 1 |

All four collected three tests. Names, order, and return counts `1, 2, 0` remained intact. The empty control expected and observed `[]` throughout. Both failures were assertion mismatches at the new JSON comparison.

Used the documented interpreter and native command:
`python -B -m pytest -vv -s -p no:cacheprovider -p observer checks_manifest.py`.
The temporary observer captured executing `write_manifest` frames and persisted JSON inside each test process, confirming each phase’s own copied `manifest.py`. Source SHA-256 values were:

- Correct: `f8eaac61656a4ea2508fc566a049377a9cc6c8b31969a35b81d0952ce5974476`
- Faulty: `9b10709a2fd975d20d393badfcc3be0459405db736f77078ee7b91434881cc4b`

Both parametrizations, fixtures, configuration, and empty control were preserved. Only `checks_manifest.py` changed; all other file bytes and modes matched the initial snapshot. All audit scratch was removed.
