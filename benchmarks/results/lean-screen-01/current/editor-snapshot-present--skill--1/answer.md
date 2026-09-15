I’m using the mother-in-law skill to add the two native save regressions, then run the three-test suite once and report any failures without changing production.



The existing `writes()` helper provides callback-entry observation, delayed serialization, and task cleanup. `Editor.save` currently copies only the outer dictionary; the pending-payload assertion will check whether a later theme edit changes its nested snapshot.



Added exactly two tests in `test_editor.py`; preserved the initial-state test and production code.

One native suite run: **2 passed, 1 failed**.

Under `test_editor.EditorTests`:

- `test_initial_state`: PASS.
- `test_save_without_intervening_edit_marks_clean`: PASS; acknowledged settings are stored correctly and marked clean.
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL; the pending payload changed from `dark` to `solarized` after the live edit.

The regression failure remains intact. Cleanup completed; the adversarial post-acknowledgement assertions exist but were not reached.

Tested real `Editor.save` through native async unittest, using deterministic gates and delayed serialization. No browser or real storage was tested.

Complete bounded command (15-second suite timeout; 1-second async waits):

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```
