I’ll use the mother-in-law skill to add the two native save regressions, then run the three-test suite once and retain any production failures.

The existing fixture provides callback-entry observation, delayed copying after acknowledgement, and task cleanup. `Editor.save` currently makes a shallow copy, so the adversarial test will check the full pending payload after a second theme edit, then check stored and live state if that assertion passes.

The tests are added. The first command could not start because `python` is unavailable; I’ll use `python3`. No tests have run yet.

Added exactly two methods to `test_editor.py`; preserved the initial test and production code.

One native suite run:

- `test_editor.EditorTests.test_initial_state`: PASS
- `test_editor.EditorTests.test_save_without_intervening_edit_marks_clean`: PASS
- `test_editor.EditorTests.test_save_snapshot_survives_intervening_edit`: FAIL

The normal save stores the full expected settings and becomes clean. The adversarial test demonstrates that changing the theme to `sepia` mutates the pending payload, which should retain `dark`. Its later stored/current/dirty assertions remain present but were not reached; fixture cleanup handled the pending task.

Tested real `Editor.save` through `unittest`, with deterministic gates and delayed serialization. No browser or real storage was tested.

Complete bounded command:
```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15).returncode)'
```

The earlier `python` command failed to launch because that executable was unavailable. The regression failure is retained.
