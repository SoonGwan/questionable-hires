I’ll use the mother-in-law skill to add the two native save regressions, using the existing controlled-write support, then run the three-test suite once and retain any regression failure.

The existing helper records a deep copy only after acknowledgement, as required. `Editor.save` currently copies only the outer dictionary, so the pending-payload assertion should expose whether a later theme edit changes the save snapshot. Both tests will use full, independent expected values and bounded waits.

The tests are added. The first command could not launch because `python` is unavailable; I’ll use `python3` for the suite’s single execution.

Added exactly two tests to `test_editor.py`; preserved the initial test and production code.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme to `solarized` mutates the pending full payload, which should retain `dark`. Cleanup completed; post-acknowledgement assertions remain present but were not reached in that case.

Tested real `Editor.save` through unittest with controlled callback entry, delayed serialization, one-second waits, and owned-task cleanup. No external persistence or UI was tested.

Suite executed once: `python3 -B -m unittest -v test_editor`. Earlier launch with `python` failed because that executable was unavailable. Regression failure retained.
