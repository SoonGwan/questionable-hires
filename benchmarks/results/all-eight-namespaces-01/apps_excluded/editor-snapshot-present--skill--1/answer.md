I’ll use the mother-in-law skill to add the two native save regressions, reuse the controlled writes fixture, and run the three-test suite once without changing production.


The fixture already provides callback-entry observation, delayed deep-copy recording after acknowledgement, bounded waits, and task cleanup. `Editor.save` currently makes a shallow copy, so the pending-payload assertion should expose nested settings changing during a save.


The tests are written. The first command could not start because `python` is unavailable; I’ll use `python3` for the suite’s single run.


Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_snapshot_survives_intervening_edit`: FAIL

The failure demonstrates that changing the live theme to `blue` also changes the pending nested payload, which should retain `dark`. Cleanup ran; post-acknowledgement assertions remain present but were not reached in that case.

Tested real `Editor.save` using deterministic, bounded async gates and delayed serialization. No browser or external persistence was tested.

Suite ran once using:
```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=10).returncode)'
```

The earlier `python` invocation failed before running tests because that executable was unavailable.
