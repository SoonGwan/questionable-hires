I’ll inspect the tests and package bindings, run the native tests on correct and faulty code, then check archive metadata and input preservation with a stronger assertion if needed. I’ll restore all original bytes and modes afterward.

The two native tests check entry order, CRC validity, and an empty archive, but do not assert permissions, creator system, exact payload bytes, or input preservation. The public entrypoint delegates through an imported `_pack` alias. I’ll verify both bindings in each test process and test the single-line omission in disposable project-local copies.

The existing native tests **miss the fault**.

| Version | Existing tests | Stronger assertion |
|---|---|---|
| Correct | 2 passed | Passed |
| Only `external_attr` assignment omitted | 2 passed | Assertion failure: both permissions became `0o600`, versus `0o755` and `0o640` |

The stronger check reopened real `create_package` output and compared complete ordered records. Payloads, filenames, Unix creator system, and input preservation passed in both versions.

Verified the actual test’s `build` binding and endpoint’s `_pack` binding in each checking process. No import/setup errors occurred.

Original bytes and modes were preserved; disposable copies were removed. No repairs or permanent harness/report remain.
