I’m using the mother-in-law skill to add the two native save regressions, with controlled acknowledgement and delayed serialization. I’ll read the project instructions and test support, then run the three-test suite once, preserving any regression failures.


The existing `writes()` helper provides the required gates and copies the payload only after acknowledgement. `Editor.save` currently makes a shallow copy, so the pending-payload assertion will check whether a later theme edit leaks into its nested settings.


The tests are added. The first command could not start because this environment has no `python` executable. I’ll use `python3` to run the suite with the same 10-second bound.


Added exactly two tests in `test_editor.py`; preserved the initial test and production code.

One native suite run: **2 passed, 1 failed**. Identities under `test_editor.EditorTests`:

- `test_initial_state` — PASS.
- `test_save_without_intervening_edit_marks_clean` — PASS: acknowledged save stores full settings and becomes clean.
- `test_save_snapshot_survives_intervening_theme_edit` — FAIL: pending payload changes from `dark` to `solarized`.

The regression failure remains. Its post-acknowledgement checkpoints exist but were not reached; owned-task cleanup completed.

Tested real `Editor.save` through native unittest with controlled persistence, delayed serialization and one-second waits. No browser or real storage tested.

Bounded command:
```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_editor"], timeout=10).returncode)'
```

The initial `python` invocation failed before running tests because that executable was unavailable.
