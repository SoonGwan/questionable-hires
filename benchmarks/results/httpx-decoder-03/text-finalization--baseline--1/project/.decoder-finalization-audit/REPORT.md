# UTF-8 stream finalization audit

Coverage gap confirmed in tests/test_decoders.py.

The sole behavioral mutation changes TextDecoder.flush() from
self.decoder.decode(b"", True) to self.decoder.decode(b"", False).
This leaves an incomplete UTF-8 sequence buffered at EOF instead of emitting U+FFFD.

Results:
- Existing test_decoders.py: correct 40 passed; faulty 40 passed.
- Focused assertions: correct 4 passed; faulty 2 failed, 2 passed.
- Both sync iter_text() and async aiter_text() (asyncio) were exercised.
- Incomplete chunks (b"prefix \xe2", b"\x82") must yield "prefix \ufffd";
  the mutant yields "prefix ". Both focused incomplete cases detect this.
- Valid split control (b"prefix \xe2", b"\x82\xac") yields "prefix €"
  with both implementations.

Existing test_streaming_text_decoder (line 296) uses ASCII only.
The UTF-8 autodetect case (line 244) has complete input and calls aread()
before aiter_text(), so it does not protect incomplete multibyte EOF behavior.

All runs used /tmp/qh-httpx-preflight.3Slnqw/venv/bin/python, with bytecode
and pytest cache writing disabled. run_checks.py asserts that each run imports
its own copied httpx. Commands and exit codes are recorded in runs.json;
full outputs are in the four *.log files; mutation.diff records the sole change.
Original httpx/ and tests/ file hashes and file sets verified unchanged.
The two copies differ only in httpx/_decoders.py.
