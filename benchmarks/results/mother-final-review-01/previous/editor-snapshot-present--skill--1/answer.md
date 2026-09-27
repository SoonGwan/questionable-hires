I’ll read the mother-in-law skill and project files, add the two regression tests, and run the three-test suite once. I’ll leave production code unchanged and retain any regression failures.

The existing helper provides the required gates, delayed serialization, and task cleanup. `Editor.save` makes a shallow copy, so I expect the pending-payload assertion to expose a nested snapshot failure. I’ll check the full payload and include all required post-completion checks in both tests.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Ran once:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_editor
```
Callback entry, completion, and cleanup use one-second bounds.

Results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_retains_snapshot_and_newer_edit_stays_dirty`: FAIL

The failure demonstrates that changing the live theme to `solarized` also changes the pending snapshot, which should retain `dark`. The regression remains failing.

Coverage exercises real `Editor.save` through native async unittest with delayed serialization. The failing assertion triggers cleanup before acknowledgement; subsequent stored/current/dirty checks exist but were not reached. No browser or external persistence was tested.
