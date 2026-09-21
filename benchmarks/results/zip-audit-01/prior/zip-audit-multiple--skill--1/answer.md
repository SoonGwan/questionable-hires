I’ll read the con-artist skill and trace the tests, entrypoint, and writer, then check each fault independently and remove the disposable copies.

The tests check entry names/order and CRC consistency, but never compare payloads or permissions with the inputs. Both faults could therefore pass. I’ll run the native suite and a stronger record comparison through the real `create_package`, verifying both bindings in each test process.

Both independent faults survive the existing native tests.

| Version | Existing tests | Stronger assertion |
|---|---|---|
| Correct code | 2 passed, exit 0 | Passed, exit 0 |
| Omit only `external_attr` assignment | 2 passed, exit 0 | Assertion failure: permissions `0600/0600`, expected `0755/0640` |
| Write `b''`, preserving metadata | 2 passed, exit 0 | Assertion failure: binary payload empty, expected `b'\x00\xfflaunch'` |

Executed `python3 -B -m unittest -v test_package` and the temporary stronger unittest in isolated project-local copies. The successful correct-code observations were reused for the second fault.

Every check process verified the actual tests’ `build` binding to public `create_package`, and the endpoint’s `_pack` binding to the copied writer.

The stronger test reopened the real endpoint’s returned bytes, compared complete ordered `(filename, payload, permission bits, creator system)` records for both entries, and verified input preservation. Both mutant failures were defect-specific assertions; no import/setup errors occurred.

The gap: names and CRC consistency do not establish intended payloads or permissions. Original bytes/modes and project inventory remained unchanged; all owned disposable copies were removed. No repairs, harness, or report retained.
