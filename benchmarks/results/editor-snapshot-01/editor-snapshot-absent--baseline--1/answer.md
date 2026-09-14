I’ll read the project instructions and existing tests, add the two gated async regression tests, then run the three-test suite once and preserve any production failures.

`Editor.save` makes a shallow copy, so the nested display settings appear to remain shared while persistence is pending. I’ll use events to observe callback entry and control acknowledgement, with the persist double copying its payload only after acknowledgement.

Added exactly two tests; preserved the initial-state test and production code.

Ran `python3 -m unittest -v test_editor` once. Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme mutates the full pending payload before acknowledgement. Cleanup cancelled the pending save; subsequent stored/current/dirty assertions remain present but were not reached.

Coverage exercises real `Editor.save` through native async unittest, with deterministic gates, bounded waits, and delayed deep-copy serialization. It does not exercise an external persistence backend.
