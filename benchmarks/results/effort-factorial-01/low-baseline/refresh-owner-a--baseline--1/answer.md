I’ll check `Preview.refresh` against the requirements, add controlled-callback tests, and run the requested unittest command.


`refresh` clears `pending` whenever any call settles, so an older call can incorrectly clear it while the latest call is still running. I’ll guard that cleanup by generation and test overlapping calls using events and futures, without timing sleeps.


Fixed `preview.py`: only the latest-started refresh may clear `pending`.

Added `test_preview.py` covering all requested scenarios with actual `Preview` instances, controlled callbacks, bounded waits, task cleanup, and no timing sleeps. Overlapping calls remain concurrent. Requirements and owner notes are unchanged.

Ran `python3 -B -m unittest discover -v` twice. Both native runs reported:

```text
Ran 5 tests in 0.038s

OK
```

Both test processes exited with code `0`.
