I’ll read the project instructions and test support, add the two regression tests, and run the three-method native suite once, preserving any regression failures.


`writes()` provides callback-entry observation, bounded waits, delayed deep-copy storage, and task cleanup. `Editor.save()` currently makes a shallow copy, so I expect the intervening-edit test to expose mutation of the pending nested payload.


Added exactly two tests in `test_editor.py`; preserved the initial-state test and production files.

Ran `python3 -m unittest -v test_editor` once. Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_keeps_newer_edit_dirty`: FAIL

The failure demonstrates that changing the live theme to `blue` mutates the pending full payload, which should retain `dark`.

Coverage exercises real `Editor.save` with deterministic callback gates, delayed serialization, bounded waits, and failure-safe cleanup. The failing assertion prevents subsequent completion checks from executing; those checkpoints remain present. Persistence is simulated in memory; no external storage is tested.
