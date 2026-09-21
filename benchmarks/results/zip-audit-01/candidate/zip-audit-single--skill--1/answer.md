I’ll read the con-artist skill and trace the tests, public entrypoint, and writer, then run the isolated mutation and stronger assertion checks.

The two existing tests check entry names and CRC validity, but not payload contents or metadata. I’ll remove only the `external_attr` assignment in a disposable copy, run both tests, then check complete ZIP records and input preservation on correct and faulty code. Each run will verify the test’s `build` binding and the endpoint’s `_pack` binding in the same process.

The existing tests **miss the fault**.

| Native unittest checks | Correct code | Only `external_attr` assignment omitted |
|---|---|---|
| Both existing tests | PASS | PASS |
| Stronger complete-record assertion | PASS | FAIL: permission mismatch |

The stronger check reopened bytes from the real `create_package` and compared ordered `(filename, payload bytes, permission bits, Unix creator system)` records. Faulty permissions were `0o600` for both entries instead of `0o755` and `0o640`. Payloads, order, creator system, and inputs remained intact.

Every run verified the actual test’s `build → create_package` and endpoint’s `_pack → writer.pack` bindings in the same process. The failure was an assertion failure, with no import/setup errors.

All disposable copies were removed. Original file bytes and modes were verified unchanged; no repairs or permanent harness/report retained.
