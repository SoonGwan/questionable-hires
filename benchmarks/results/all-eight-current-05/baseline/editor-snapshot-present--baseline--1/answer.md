I’ll read the project instructions and test support, add the two regression tests, then run the three-test suite once and retain any regression failures.

The existing `writes()` helper provides callback-entry observation, delayed deep-copy storage, bounded waits, and task cleanup. `Editor.save` currently makes a shallow copy, so I expect the pending nested payload check to expose the regression. I’ll use independent full-payload expectations in both tests.

The tests are written. The first launch attempt failed because `python` is unavailable; no tests ran. I’ll run the suite with `python3`.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

One native suite run: **3 tests, 2 passed, 1 failed**. Under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_snapshot_and_keeps_newer_edit_dirty`: FAIL

The failure demonstrates that changing the live theme to `blue` mutates the pending snapshot expected to contain `dark`. Cleanup ran; subsequent acknowledgement and completion assertions remain present but were not reached.

Coverage exercises real `Editor.save` through `unittest`, with deterministic callback gates and delayed serialization. It does not test external storage.

The initial `python` launch was unavailable; `python3` executed the suite. Both attempts remain recorded.
