I’ll read the project instructions and test helpers, add the two regression tests, then run the three-method suite once, preserving any regression failures.

`Editor.save` shallow-copies the settings, so its pending payload shares nested values with live settings. The existing `writes()` helper provides the required gates, delayed deep copy, and task cleanup. I’ll use it to check both clean completion and snapshot isolation during a pending save.

Added exactly two native tests to `test_editor.py`, preserving the initial-state test and production code.

Ran `python3 -m unittest -v test_editor` once. Under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_leaves_newer_edit_dirty`: FAIL

The failure demonstrates that changing the live theme to `solarized` mutates the pending snapshot, which should retain `dark`.

Coverage exercises real `Editor.save` with full nested payload comparisons, deterministic callback gates, delayed serialization, bounded waits, and owned task cleanup. No external persistence is exercised. The failing assertion unwound to cleanup; subsequent stored/current/dirty checkpoints remain present but were not reached in that test.
