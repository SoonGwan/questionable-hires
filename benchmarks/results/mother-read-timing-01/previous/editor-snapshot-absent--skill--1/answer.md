I’ll use the mother-in-law skill to add deterministic interaction tests for `Editor.save`, then run the three-test suite and preserve any regression failures.


`Editor.save` makes a shallow copy, so a later theme edit appears able to change the pending payload. I’ll add a persist double that exposes the actual callback argument and waits for acknowledgement before deep-copying it into storage. The tests will check both save sequences and clean up the save task even if an assertion fails.


The first launch failed because `python` is unavailable; no tests ran. I’ll use `python3` for the suite run.


Added exactly two tests in `test_editor.py`, preserving the initial-state test and production code.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_snapshot_survives_edit_while_persist_pending`: FAIL

The failure demonstrates that changing the theme to `solarized` mutates the pending nested payload, which should retain `dark`. Cleanup completed; subsequent acknowledgement and completion assertions remain present but were not reached.

Tests exercise real `Editor.save` using deterministic gates, delayed serialization, independent full-payload expectations, and bounded waits. This covers the Python interaction layer, not browser or real storage behavior.

Suite ran once using:
```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```

The initial `python` launch failed before running tests because that executable was unavailable. Both attempts remain in captured output.
