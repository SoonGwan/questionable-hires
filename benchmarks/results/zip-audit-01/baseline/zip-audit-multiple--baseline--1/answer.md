I’ll inspect the tests and package bindings, then run the correct code and each fault independently. I’ll restore the source afterward and remove any disposable files I create.


Both existing tests check entry names and ZIP CRC validity, but neither compares payloads or permissions. I’ll use isolated project-local copies for each fault, verify both bindings in each test process, and add a temporary assertion using the binary and empty records from the actual test.


Both independent faults escape the existing native tests.

| Version | Existing tests | Identical stronger assertion |
|---|---|---|
| Correct | 2 passed | Passed |
| Omit `external_attr` assignment | 2 passed | Assertion failure: both permissions became `0o600`, instead of `0o755` / `0o640` |
| Write `b''`, preserve metadata | 2 passed | Assertion failure: binary payload became empty; metadata remained correct |

Each process verified the actual test’s `build` binding to public `create_package` and the endpoint’s `_pack` binding to the modified writer.

The stronger test reopened returned bytes and compared complete ordered filename/payload/permission/creator records using the existing fixture. Input preservation passed throughout. Failures were defect-specific assertions, with no setup/import errors.

Original bytes and modes were preserved; all owned disposable copies were removed. No repairs or permanent harness/report were retained.
