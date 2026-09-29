I’ll read the mother-in-law skill and project tests, add the two regression cases, and run the three-test suite once, preserving any production failures.

The existing `writes()` helper provides the required gates, delayed deep copy, and task cleanup. `Editor.save()` currently makes a shallow copy, so the pending-payload check should expose nested settings changing during a save. I’ll also cover the normal save becoming clean after acknowledgement.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production files.

Ran once:
```sh
/opt/homebrew/bin/python3 -B -m unittest -v test_editor
```
Exit: **1**. Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_pending_snapshot_and_newer_dirty_edit`: FAIL

The normal save stores the full expected settings and becomes clean. The regression demonstrates that changing the live theme to `blue` also changes the pending payload, which should retain `dark`.

Coverage exercises real `Editor.save` through unittest with callback-entry gates, one-second bounded waits, delayed serialization, and failure-safe cleanup. The failing assertion prevents subsequent acknowledgement and completion checks from executing; those checks remain in place. No browser or external persistence was tested.
