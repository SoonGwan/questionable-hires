I’ll read the mother-in-law skill and project tests, then add the two regression cases with deterministic gates and run the three-test suite once.

`Editor.save` makes a shallow copy, so its pending payload shares nested settings with the editor. I’ll use a minimal persist double that observes callback entry and deep-copies the payload only after acknowledgement. The tests will check both the clean completion path and whether an intervening edit mutates the pending snapshot.

Added exactly two tests in `test_editor.py`; preserved the initial-state test and production code.

One native suite run:
- `test_editor.EditorTests.test_initial_state`: PASS
- `test_editor.EditorTests.test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_editor.EditorTests.test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme to `solarized` also changes the pending snapshot, which should retain `dark`. Cleanup completed; subsequent acknowledgement and completion assertions remain present but were not reached.

Tested real `Editor.save` with deterministic callback-entry and acknowledgement gates, delayed deep-copy serialization, and bounded waits. No browser or real storage was tested.

Complete command (15-second process bound):
```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```
