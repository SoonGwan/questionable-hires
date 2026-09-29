I’ll read the skill, project instructions, and existing tests, then add the two gated regressions and run the three-test suite once. I’ll preserve any production regression failures.

I’m applying the mother-in-law skill. The existing `writes()` helper provides callback-entry observation, delayed deep-copy serialization, and task cleanup. `Editor.save` currently makes a shallow copy, so the pending-payload assertion should expose nested settings changing after save entry.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

One run, native identities under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_keeps_newer_edit_dirty`: FAIL

The failure demonstrates that changing the live theme to `solarized` mutates the pending full payload, which should retain `dark`. Cleanup completed; subsequent acknowledgement and final-state assertions exist but were not reached in the failing case.

Tested real `Editor.save` through native unittest with controlled persistence, delayed serialization, bounded waits, and owned-task cleanup. No browser or real storage was tested.

Complete command, bounded to 15 seconds:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```
