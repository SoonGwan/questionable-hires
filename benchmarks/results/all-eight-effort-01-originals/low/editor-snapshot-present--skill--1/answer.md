I’m using the mother-in-law skill to add the normal-save and pending-save regression cases, then run the native suite once. I’ll leave production code unchanged and retain any regression failure.


The tests are added. The first command could not start because `python` is unavailable; I’ll use `python3` to run the suite. The existing helper provides callback-entry gates, delayed serialization, and task cleanup.


Added exactly two tests in `test_editor.py`; preserved the initial test and production code.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_snapshot_survives_intervening_theme_edit`: FAIL

The failure demonstrates that changing the theme to `blue` mutates the pending full payload, which must retain `dark`. The assertion unwound to task cleanup; subsequent acknowledgement and final-state checkpoints remain present but were not reached.

Tested real `Editor.save` with controlled persistence, delayed deep-copy serialization, and one-second bounded waits. No browser or external storage was tested.

Suite ran once:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_editor
```

The earlier invocation using `python` failed to launch because that executable was unavailable.
