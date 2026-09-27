I’m using the mother-in-law skill to add two deterministic async regression tests, preserving the initial-state test and production code.

`Editor.save` makes a shallow copy, so a later theme edit appears able to change the pending payload. I’ll have the persist double copy its argument only after acknowledgement, and check the full payload while it is still pending.

Added exactly two tests in `test_editor.py`; preserved the initial test and production code.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_pending_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the theme to `blue` mutates the pending snapshot expected to retain `dark`. Later completion assertions remain present but were not reached; cleanup cancelled and drained the task.

Coverage exercises real `Editor.save` with deterministic callback gates, delayed deep-copy serialization, and bounded waits. It does not cover browser or external persistence behavior.

The three-method suite ran once:
```sh
python3 -B -c 'import signal, unittest; signal.alarm(15); unittest.main(module="test_editor", verbosity=2)'
```

An earlier launch using `python` failed because that executable was unavailable.
