I’m using the mother-in-law skill to add deterministic save regression tests, then run the three-test native suite once and report any failures without changing production.


The existing fixture already provides delayed serialization and task cleanup. `Editor.save` makes a shallow copy of settings, so I expect the nested theme edit to mutate the pending payload. The tests will check that payload before acknowledgement and include checks for stored and live state after completion.


Added exactly two tests; preserved the initial-state test and production code.

Ran `python3 -m unittest -v test_editor` once. Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The pending full payload changed from `dark` to `solarized` before acknowledgement, demonstrating broken snapshot isolation.

Coverage exercises real `Editor.save` with deterministic gates, delayed serialization, bounded waits and owned-task cleanup. The failing assertion unwound to cleanup; post-acknowledgement assertions remain present but were not reached in that test. No browser or external persistence was tested.
