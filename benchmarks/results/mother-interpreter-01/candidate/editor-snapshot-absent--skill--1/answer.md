I’ll read the mother-in-law skill and project tests, add the two gated regressions, then run the three-method suite once. I’ll leave production code unchanged and preserve any regression failure.

`Editor.save` makes a shallow copy, so its nested payload appears vulnerable to later theme edits. I’ll use a minimal persist double that signals callback entry, waits for acknowledgement, and only then deep-copies the received payload to model delayed storage. Each test will own and clean up its save task.

Added exactly two tests and minimal gated persist support in `test_editor.py`; preserved the initial test and production code.

One native run, exit **1**. Identities under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_clean`: PASS
- `test_save_preserves_snapshot_and_newer_dirty_edit`: FAIL

The failure demonstrates that changing the live theme to `sepia` mutates the pending payload, which should retain `dark`. The full nested payload assertion caught it. Cleanup completed; subsequent acknowledgement and final-state checkpoints remain present but were not reached in the failing case.

Tested real `Editor.save` through `unittest.IsolatedAsyncioTestCase`, with delayed-copy persistence, deterministic gates and one-second waits. No browser or real storage was tested.

Complete command, bounded to 15 seconds:

```sh
/opt/homebrew/bin/python3 -B -c 'import subprocess, sys; sys.exit(subprocess.call([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=15))'
```
