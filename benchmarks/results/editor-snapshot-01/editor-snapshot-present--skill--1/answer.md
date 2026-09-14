I’ll use the mother-in-law skill to add the two gated save regressions, then run the native suite once and retain any production failures.

The existing helper provides callback-entry observation and delayed deep-copy storage. `Editor.save` currently makes a shallow copy, so the pending-payload assertion should expose nested settings changing during a save. I’ll use full, independent expected payloads and bounded completion waits in both tests.

Added exactly two tests to `test_editor.py`; preserved the initial-state test and production code.

Ran once: `python3 -B -m unittest -v test_editor`  
Callback entry, completion, and cleanup waits are bounded to one second.

Native results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_preserves_pending_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme to `solarized` mutates the pending full payload, which should retain `dark`. The normal save stores the expected settings and becomes clean.

Tested real `Editor.save` with controlled, delayed serialization. The failing assertion unwound safely before acknowledgement; post-completion assertions remain present but were not reached in that case. No browser or external persistence was tested.
