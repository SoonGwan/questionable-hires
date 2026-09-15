I’ll read the project instructions and test support, add the two regression tests, then run the three-test suite once and retain any regression failures.

`Editor.save` makes a shallow copy, so the pending payload shares nested settings with the live editor. The supplied `writes()` helper supports the required delayed copy and task cleanup. I’ll test that isolation boundary and the no-edit completion case.

Added exactly two tests in `test_editor.py`; preserved the initial-state test and production files.

Ran once: `python3 -m unittest -v test_editor`

Native results under `test_editor.EditorTests`:

- `test_initial_state` — PASS
- `test_save_without_intervening_edit_marks_settings_clean` — PASS
- `test_save_preserves_snapshot_and_keeps_newer_edit_dirty` — FAIL

The failure demonstrates that changing the live theme to `blue` also changes the pending full payload, which should retain `dark`.

Coverage exercises real `Editor.save` using native async unittest, deterministic callback gates, delayed serialization, bounded waits, and owned task cleanup. No external persistence is exercised. The failing pending-payload assertion unwinds to cleanup; subsequent stored/current/dirty checkpoints exist but were not reached.
