I’m using the mother-in-law skill to add the two save-sequence regressions, then run the native suite once. I’ll preserve production code and report any regression failures.



The existing `writes()` helper provides delayed serialization, callback-entry observation, and task cleanup. `Editor.save` currently copies only the outer dictionary, so the pending-payload assertion should catch nested settings changing during a save.



The tests are added. The first command could not start because `python` is unavailable; I’ll use `python3` to run the suite. No tests ran in that attempt.



Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme to `solarized` mutates the pending full payload, which should retain `dark`. Cleanup ran; subsequent acknowledgement and final-state checkpoints remain present but were not reached.

Tested real `Editor.save` through native unittest with controlled persistence, delayed serialization, one-second waits, and owned-task cleanup. No browser or external storage was tested.

The suite ran once using this bounded command:
```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```

The earlier `python` launch failed before running tests. The regression failure remains intact.
