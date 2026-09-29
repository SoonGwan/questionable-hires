I’ll read the mother-in-law skill and project tests, add the two regression cases, then run the three-test suite once. Production code will remain unchanged.

The existing `writes()` helper provides callback-entry observation, acknowledgement gates, delayed deep-copy recording, and task cleanup. `Editor.save` currently makes a shallow copy, so the pending-edit case should expose nested payload mutation. I’ll assert the full payload while pending and include all requested post-completion checks.

Added exactly two tests to `test_editor.py`, preserving the initial-state test and production code.

One suite run, native identities under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_pending_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme to `solarized` mutates the pending full payload, which should retain `dark`. Cleanup completed; subsequent acknowledgement and final-state assertions remain present but were not reached.

Coverage exercises real `Editor.save` with deterministic gates, delayed serialization, one-second waits, and owned-task cleanup. No browser or real storage was tested. Scoped diff review passed.

Complete command, bounded to 15 seconds:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```
