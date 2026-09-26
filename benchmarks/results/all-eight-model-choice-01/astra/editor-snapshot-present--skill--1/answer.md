I’ll use the mother-in-law skill to add the two gated save regressions, preserve the initial-state test, and run the native suite once without changing production code.


The existing `writes()` helper provides the required gates and delayed deep copy. `Editor.save` currently makes a shallow copy, so I expect the intervening theme edit to change the pending payload. The new tests will check the full nested payload and post-completion state.


Added exactly two methods to `test_editor.py`; preserved the initial-state test and production files.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the theme while persistence is pending mutates the nested pending payload from `dark` to `solarized`. Cleanup completed; subsequent acknowledgement and final-state assertions remain present but were not reached.

Tested real `Editor.save` through native unittest with deterministic gates, delayed serialization, one-second waits, and owned-task cleanup. No UI or external storage was tested.

The suite ran once using:
```sh
python3 -B -c 'import signal, unittest; signal.alarm(10); unittest.main(module="test_editor", verbosity=2)'
```
An earlier launch using `python` failed because that executable was unavailable; it ran no tests.
