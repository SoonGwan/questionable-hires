I’ll read the skill and project files, add the two gated async regression tests, and run the native suite once. Production code will remain unchanged.

I’m applying the mother-in-law skill to the pending-save sequence. `Editor.save` currently makes a shallow copy, which leaves nested settings shared. The test double will retain the actual payload and copy it only after acknowledgement, so the test can expose that behavior.

Added exactly two tests and minimal gated support to `test_editor.py`; preserved the initial test and production code.

One native run, under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_newer_edit_remains_dirty`: FAIL

The failure demonstrates that changing the live theme to `solarized` also changes the pending full payload, which should retain `dark`. Cleanup completed. Post-acknowledgement assertions exist but were not reached in the failing case.

Tested real `Editor.save` through `unittest`, with delayed serialization, deterministic gates, one-second waits and task cleanup. No browser or external persistence was tested.

Complete command, run once with a 15-second deadline:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```

The regression failure remains intact.
