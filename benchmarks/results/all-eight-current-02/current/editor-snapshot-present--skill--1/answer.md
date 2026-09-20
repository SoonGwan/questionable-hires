I’ll use the mother-in-law skill to add the two native save regressions, then run the three-test suite once and report any failures without changing production.

The existing `writes()` helper provides callback-entry observation, delayed serialization and task cleanup. `Editor.save` currently makes a shallow copy, so I’ll check whether a theme change mutates the nested payload while persistence is still pending, as well as the required states after acknowledgement.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Single native run: **2 passed, 1 failed**.

- `test_editor.EditorTests.test_initial_state` — PASS.
- `test_editor.EditorTests.test_save_without_intervening_edit_marks_settings_clean` — PASS: acknowledged save stores full expected settings and marks them clean.
- `test_editor.EditorTests.test_save_preserves_snapshot_and_leaves_newer_edit_dirty` — FAIL: changing theme to `sepia` mutates the pending payload, which should retain `dark`.

Tested real `Editor.save` through `unittest`, using controlled persistence, delayed deep-copy serialization, bounded waits and owned-task cleanup. The failing assertion unwinds to cleanup; subsequent stored/current/dirty checkpoints exist but were not reached.

Complete command (10-second bound):

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=10).returncode)'
```

Coverage is at the Python application layer; no real storage or browser was exercised.
