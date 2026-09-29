I’m using the mother-in-law skill to add the two gated regression tests, then run the three-test suite once and report any failures without changing production.


The existing helper observes callback entry and deep-copies the payload only after acknowledgement. `Editor.save` currently makes a shallow copy, so the pending-payload checkpoint should expose nested settings changing during persistence.


Added exactly two methods to `test_editor.py`; preserved the initial test and production code.

Single suite run results under `test_editor.EditorTests`:

- `test_initial_state`: PASS
- `test_save_without_intervening_edit_marks_settings_clean`: PASS
- `test_save_snapshot_survives_intervening_edit`: FAIL

The failure demonstrates that changing the live theme to `blue` also changes the still-pending nested payload, which should retain `dark`. Cleanup ran; post-acknowledgement assertions remain present but were not reached in that case.

Tested real `Editor.save` through native unittest with controlled persistence, delayed serialization, bounded waits, and owned-task cleanup. No browser or real storage was tested.

Complete command, bounded to 10 seconds:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=10).returncode)'
```
