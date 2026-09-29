I’m using the mother-in-law skill to add the two native save-sequence tests. I’ll read the editor, test support, and project instructions, then run the three-method suite once.

The provided `writes()` helper already gives each test an observed callback entry, a release gate, delayed serialization, and task cleanup. I’ll use it directly and assert complete nested settings with separate expected values.

The first test command could not start because this environment has no `python` executable. I’ll run the same three-method suite with `python3`; the tests and assertions are unchanged.

Added exactly two native `Editor.save` regression tests in [test_editor.py](project/test_editor.py), preserving the initial-state test. They use controlled callback entry, acknowledgement, delayed serialization, bounded waits, and task cleanup.

The three-method suite ran once with `python3 -c 'import signal, unittest; signal.alarm(10); unittest.main(module="test_editor", verbosity=2)'`: **2 passed, 1 failed**. A save with no intervening edit stored the full nested settings and became clean. In the intervening-edit case, the still-pending payload changed from `dark` to `blue`, violating the per-save snapshot contract. That assertion stopped the test before its post-acknowledgement checks; those checks remain in place for conforming production.

This is native `Editor.save` coverage only. Production code was not changed.
