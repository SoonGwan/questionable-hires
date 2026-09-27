I’ll use the mother-in-law skill to add the two gated regression tests, then run the three-test suite once and report any failures without changing production code.

The existing `writes()` helper provides the required gates and copies the payload only after acknowledgement. `Editor.save` currently makes a shallow copy, so the pending-payload assertion should expose nested settings changing during the save. Both tests will include the required completion checks.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Single native run: **2 passed, 1 failed**, under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_leaves_newer_edit_dirty`: FAIL

The failure demonstrates that changing the live theme to `solarized` also changes the pending payload, which should retain `dark`. Completion checks exist but were not reached in that case; cleanup cancelled the pending save.

Coverage exercises real `Editor.save` through unittest with controlled persistence, delayed serialization, and bounded waits. No browser or real storage was tested.

Complete command, run once with a 15-second bound:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```
