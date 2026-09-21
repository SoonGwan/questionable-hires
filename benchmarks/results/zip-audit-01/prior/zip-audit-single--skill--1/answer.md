I’ll use the con-artist skill to inspect the bindings, run the native tests, and check the isolated permission fault with the stronger assertion you specified.

The tests check entry names and CRC validity, but neither checks permissions or input preservation. The public entrypoint calls `endpoint._pack`, which is bound to `writer.pack`. I’ll verify those bindings in each test process and remove only the `external_attr` assignment in the isolated faulty copy.

The native tests **miss the fault**: removing only `pack`’s `external_attr` assignment leaves both tests passing. Payload writing remained unchanged.

All four isolated runs used `python3 -B -m unittest -v test_package`:

| Assertions | Correct code | Faulty code |
|---|---|---|
| Existing tests | 2 passed | 2 passed |
| Stronger assertions | 2 passed | 1 passed, 1 assertion failure |

Each process verified the actual tests’ `build` binding to public `create_package`, and the endpoint’s `_pack` binding to `writer.pack`.

The stronger test reopened the returned ZIP bytes and compared complete ordered records, including binary/empty payloads, permissions, and Unix creator system. The fault produced `0o600` for both entries instead of `0o755` and `0o640`; `assertEqual(actual, expected)` failed specifically on permissions. Input-preservation checks passed on both versions. No import/setup errors occurred.

Original bytes and modes were verified unchanged. All disposable copies were removed; no harness, report, or repair was retained.
