I’ll read the project instructions and test support, add the two regression tests, then run the three-test suite once and preserve any regression failures.

The provided `writes()` helper has the needed gates and copies the payload only after acknowledgement. `Editor.save` currently makes a shallow copy, so the pending-payload check should expose whether a later theme edit leaks into the save.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Ran `python3 -m unittest -v test_editor` once. Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme to `solarized` also mutates the pending save payload, which should retain `dark`.

Coverage exercises real `Editor.save` through native async unittest, with deterministic gates, bounded waits, delayed serialization and owned-task cleanup. No actual storage I/O is tested. The failing pending-payload assertion prevents subsequent completion checks from executing; those checks remain in place.
