I’ll use the mother-in-law skill to add the two gated save regressions, then run the three-test suite once and retain any production failures.

`Editor.save` makes a shallow copy, so later theme edits can mutate its pending nested payload. I’ll assert the full payload while persistence is blocked, with the test double copying it only after acknowledgement.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Ran once:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_editor
```
All waits and task cleanup use one-second bounds.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The pending full payload changed from expected `dark` to `sepia` after the newer edit. The failure remains intact. Post-acknowledgement assertions exist but were not reached in that case; cleanup cancelled and drained the save.

Tested real `Editor.save` through native async unittest with gated, delayed serialization. No browser or external persistence was tested.
